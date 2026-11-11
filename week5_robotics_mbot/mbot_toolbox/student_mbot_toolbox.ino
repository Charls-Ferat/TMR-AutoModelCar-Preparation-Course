/*
  ============================================================================
  STUDENT TOOLBOX -- MBot MegaPi line follower on FreeRTOS
  ============================================================================
  Everything LOW-LEVEL is already done for you and ready to call:
    - the UART wire protocol (framing, CRC, packet decoding)
    - motor primitives (motorForwardLeftRun, stopMotors, lineFollowDrive, ...)
    - the 1ms hardware timer and packet-age watchdog helpers
    - mapValue / constrainValue / applyDeadzone

  Your job is to assemble these into a working FreeRTOS system by filling
  in the five "TODO" spots below. As shipped, this sketch COMPILES and
  RUNS SAFELY (the car just sits still blinking nothing) -- you are
  building up real behavior piece by piece, not debugging a blank page.

  Read the top-level README.md first -- it explains the task graph you're
  building (UART -> shared packet -> Motion -> motors, Safety watchdog,
  Collision override) before you touch any TODO.

  Stuck? ../instructor_reference_mbot_firmware/ has a complete, working
  version of this exact exercise with teaching comments -- use it to
  check your work, not to skip the exercise.

  Hardware note: MeNewRGBLed.h/.cpp and MeCollisionSensor.h/.cpp are your
  own Makeblock MegaPi wrapper classes -- copy them into this sketch's
  src/ folder (see src/README.md).
  ============================================================================
*/

#include <Arduino_FreeRTOS.h>
#include <task.h>
#include <event_groups.h>
#include <semphr.h>

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <util/atomic.h>

#include "src/MeNewRGBLed.h"
#include "src/MeCollisionSensor.h"
#include <MeMegaPi.h>

// ======================= Constants (ready to use) ===========================
// UART protocol: [SYNC][SPEED][STEER][FLAGS][CRC]
#define BAUD_RATE               115200
#define SYNC_BYTE               0xAA
#define PACKET_SIZE             5
#define COMM_TIMEOUT_MS         500UL     // no valid packet this long -> treat host as gone

#define UBRR_VALUE              ((F_CPU / (8UL * BAUD_RATE)) - 1)

// Motor control
#define MAX_TURN_CORRECTION     120
#define TURN_SPEED              120
#define TURN_180_TIME           2900
#define STOP_TIME               300
#define MIN_MOTOR_SPEED         60

// Event bits -- a FreeRTOS event group is a shared bitfield tasks can
// wait on, set and clear. Cheaper than a mutex+bool for simple flags.
#define EVENT_COLLISION         (1 << 0)
#define EVENT_COMMS_OK          (1 << 1)

// ======================= Shared data (ready to use) ==========================

typedef struct {
  uint8_t speed;
  int8_t steer;
  uint8_t flags;
} Packet;

// ---- Hardware objects ----
MeNewRGBLed rgbled_67(67, 4);
MeNewRGBLed rgbled_68(68, 4);

MeMegaPiDCMotor motor_1(1);
MeMegaPiDCMotor motor_9(9);
MeMegaPiDCMotor motor_2(2);
MeMegaPiDCMotor motor_10(10);

MeCollisionSensor collision_65(65);
MeCollisionSensor collision_66(66);

// ---- FreeRTOS objects ----
// Any task reading/writing `latestPacket` MUST do so under packetMutex.
// Any task touching the motors MUST do so under motorMutex.
Packet latestPacket = {0, 0, 0};
SemaphoreHandle_t packetMutex;
SemaphoreHandle_t motorMutex;
EventGroupHandle_t systemEvents;

volatile uint32_t lastPacketMs = 0;
volatile uint32_t msCounter = 0;

// ======================= Timer helpers (ready to use) =========================
// 32-bit reads/writes are NOT atomic on an 8-bit AVR, so anything shared
// with the Timer3 ISR goes through ATOMIC_BLOCK.

void markPacketReceived() {
  ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
    lastPacketMs = msCounter;
  }
}

uint32_t packetAgeMs() {
  uint32_t now;
  uint32_t last;

  ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
    now = msCounter;
    last = lastPacketMs;
  }

  return now - last; // unsigned subtraction: correct even across rollover
}

// ======================= Math helpers (ready to use) ==========================

int16_t mapValue(
    int16_t x,
    int16_t inMin,
    int16_t inMax,
    int16_t outMin,
    int16_t outMax) {
  return (int16_t)(
      ((int32_t)(x - inMin) * (outMax - outMin))
      / (inMax - inMin)
      + outMin);
}

int16_t constrainValue(int16_t x, int16_t minVal, int16_t maxVal) {
  if (x < minVal) {
    return minVal;
  }

  if (x > maxVal) {
    return maxVal;
  }

  return x;
}

int16_t applyDeadzone(int16_t value) {
  if (value == 0) {
    return 0;
  }

  if (value > 0 && value < MIN_MOTOR_SPEED) {
    return MIN_MOTOR_SPEED;
  }

  if (value < 0 && value > -MIN_MOTOR_SPEED) {
    return -MIN_MOTOR_SPEED;
  }

  return value;
}

// ======================= Motor primitives (ready to use) ======================
// Plain functions, no FreeRTOS involved -- call these only while holding
// motorMutex once you're inside a task.

void motorForwardLeftRun(int16_t speed) {
  motor_10.run(-speed);
}

void motorForwardRightRun(int16_t speed) {
  motor_1.run(speed);
}

void motorBackLeftRun(int16_t speed) {
  motor_2.run(-speed);
}

void motorBackRightRun(int16_t speed) {
  motor_9.run(speed);
}

void stopMotors() {
  motorForwardLeftRun(0);
  motorForwardRightRun(0);
  motorBackLeftRun(0);
  motorBackRightRun(0);
}

void rotateInPlace(int16_t speed) {
  motorForwardLeftRun(speed);
  motorBackLeftRun(speed);
  motorForwardRightRun(-speed);
  motorBackRightRun(-speed);
}

// Blocking is fine here: only call this from inside a task that is
// already holding motorMutex -- other tasks keep running normally.
void performUTurn() {
  stopMotors();
  vTaskDelay(pdMS_TO_TICKS(STOP_TIME));

  rotateInPlace(TURN_SPEED);
  vTaskDelay(pdMS_TO_TICKS(TURN_180_TIME));

  stopMotors();
  vTaskDelay(pdMS_TO_TICKS(STOP_TIME));
}

// Differential-drive steering: positive `steer` turns one way, negative
// the other -- check which is which on your car and flip the sign if needed.
void lineFollowDrive(int16_t speed, int8_t steer) {
  int16_t correction = mapValue(
      steer,
      -40,
      40,
      -MAX_TURN_CORRECTION,
      MAX_TURN_CORRECTION);

  int16_t leftSpeed = constrainValue(speed + correction, -255, 255);
  int16_t rightSpeed = constrainValue(speed - correction, -255, 255);

  leftSpeed = applyDeadzone(leftSpeed);
  rightSpeed = applyDeadzone(rightSpeed);

  motorForwardLeftRun(leftSpeed);
  motorBackLeftRun(leftSpeed);
  motorForwardRightRun(rightSpeed);
  motorBackRightRun(rightSpeed);
}

// ======================= UART (ready to use) ===================================

void UART_init(void) {
  UCSR0A = (1 << U2X0);

  UBRR0H = (UBRR_VALUE >> 8);
  UBRR0L = UBRR_VALUE;

  UCSR0B = (1 << TXEN0) | (1 << RXEN0);
  UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

void UART_sendChar(char c) {
    while (!(UCSR0A & (1 << UDRE0)));
    UDR0 = c;
}

void UART_sendString(const char *str) {
    while (*str) {
        UART_sendChar(*str++);
    }
}

uint8_t UART_available(void) {
    return (UCSR0A & (1 << RXC0));
}

uint8_t UART_readByte(void) {
    return UDR0;
}

// ======================= Packet decoder (ready to use) ==========================

uint8_t computeCRC(const uint8_t *data, uint8_t length) {
  uint8_t crc = 0;

  for (uint8_t i = 0; i < length; i++) {
    crc ^= data[i];
  }

  return crc;
}

uint8_t resyncPacketBuffer(uint8_t *buffer) {
  for (uint8_t position = 1; position < PACKET_SIZE; position++) {
    if (buffer[position] == SYNC_BYTE) {
      uint8_t remaining = PACKET_SIZE - position;
      memmove(buffer, &buffer[position], remaining);
      return remaining;
    }
  }

  return 0;
}

// Call this often (every pass of your UART task). Returns true and fills
// `packet` exactly once per complete, CRC-valid packet found.
bool receivePacket(Packet *packet) {
  static uint8_t buffer[PACKET_SIZE];
  static uint8_t index = 0;

  while (UART_available()) {
    uint8_t value = UART_readByte();

    if (index == 0) {
      if (value == SYNC_BYTE) {
        buffer[0] = value;
        index = 1;
      }
      continue;
    }

    buffer[index++] = value;

    if (index < PACKET_SIZE) {
      continue;
    }

    uint8_t receivedCRC = buffer[PACKET_SIZE - 1];
    uint8_t calculatedCRC = computeCRC(buffer, PACKET_SIZE - 1);

    if (receivedCRC == calculatedCRC) {
      packet->speed = buffer[1];
      packet->steer = (int8_t)buffer[2];
      packet->flags = buffer[3];
      index = 0;
      return true;
    }

    index = resyncPacketBuffer(buffer);
  }

  return false;
}

// ======================= 1ms hardware timer (ready to use) =======================

void setupTimer3_1ms() {
  cli();

  TCCR3A = 0;
  TCCR3B = 0;
  TCNT3 = 0;

  OCR3A = 249;                          // 16MHz / 64 prescale / 250 counts = 1000 Hz
  TCCR3B |= (1 << WGM32);
  TCCR3B |= (1 << CS31) | (1 << CS30);
  TIMSK3 |= (1 << OCIE3A);

  sei();
}

ISR(TIMER3_COMPA_vect) {
  msCounter++;
}

// ======================= FreeRTOS tasks ===========================================
//
// vUARTTask and vLEDTask are complete below, as worked examples of the
// pattern every task in this sketch follows:
//
//     TickType_t lastWake = xTaskGetTickCount();
//     while (1) {
//         ...do this task's one job, taking a mutex around any shared state...
//         vTaskDelayUntil(&lastWake, <period>);
//     }
//
// Use that same pattern for the three TODO tasks below.

void vUARTTask(void *pvParameters) {
  UART_sendString("UART");
  (void)pvParameters;
  Packet packet;
  TickType_t lastWake = xTaskGetTickCount();

  while (1) {
    uint8_t packetsProcessed = 0;

    while (receivePacket(&packet)) {
      if (xSemaphoreTake(packetMutex, portMAX_DELAY) == pdTRUE) {
        latestPacket = packet;
        xSemaphoreGive(packetMutex);
      }

      markPacketReceived();
      xEventGroupSetBits(systemEvents, EVENT_COMMS_OK);

      packetsProcessed++;
      if (packetsProcessed >= 8) {
        break; // don't let a burst of bytes starve the other tasks
      }
    }

    vTaskDelayUntil(&lastWake, 1);
  }
}

void vLEDTask(void *pvParameters) {
  UART_sendString("LEDs");
  (void)pvParameters;
  TickType_t lastWake = xTaskGetTickCount();

  while (1) {
    EventBits_t bits = xEventGroupGetBits(systemEvents);

    if (bits & EVENT_COMMS_OK) {
      rgbled_67.setColor(2, 211, 211, 211);
      rgbled_68.setColor(2, 0, 0, 0);
    } else {
      rgbled_67.setColor(2, 0, 0, 0);
      rgbled_68.setColor(2, 211, 32, 32);
    }

    rgbled_67.show();
    rgbled_68.show();

    vTaskDelayUntil(&lastWake, pdMS_TO_TICKS(200));
  }
}

// ---------------------------------------------------------------------------
// TODO 1/5: vSafetyTask -- the watchdog.
//
// Goal: if packetAgeMs() exceeds COMM_TIMEOUT_MS, the host has gone
// silent (unplugged, laptop crashed, bad cable...) -- clear
// EVENT_COMMS_OK and force the motors to stop.
//
// Hints:
//   - Use xEventGroupClearBits(systemEvents, EVENT_COMMS_OK) when timed out.
//   - This task must NEVER get stuck. Take motorMutex with a timeout of 0
//     (xSemaphoreTake(motorMutex, 0)) -- if you can't get it instantly,
//     just try again next tick instead of blocking.
//   - Follow the same while(1) { ...; vTaskDelayUntil(&lastWake, 1); }
//     shape as vUARTTask above.
// ---------------------------------------------------------------------------
void vSafetyTask(void *pvParameters) {
  UART_sendString("Safety");
  (void)pvParameters;
  TickType_t lastWake = xTaskGetTickCount();

  while (1) {
    // TODO: check packetAgeMs() against COMM_TIMEOUT_MS.
    // TODO: if timed out, clear EVENT_COMMS_OK and (best-effort) stop the motors.

    vTaskDelayUntil(&lastWake, 1);
  }
}

// ---------------------------------------------------------------------------
// TODO 2/5: vMotionTask -- turn the latest packet into motor output.
//
// Goal: when (and only when) EVENT_COMMS_OK is set AND EVENT_COLLISION is
// NOT set, read the latest packet and call lineFollowDrive(speed, steer).
// Otherwise, keep the motors stopped.
//
// Hints:
//   - Read EventBits_t bits = xEventGroupGetBits(systemEvents); and check
//     (bits & EVENT_COMMS_OK) && !(bits & EVENT_COLLISION).
//   - Copy latestPacket out under packetMutex before using it -- never
//     read the shared global directly.
//   - Take motorMutex (portMAX_DELAY is fine here) before calling
//     lineFollowDrive or stopMotors.
//   - Subtlety worth discussing in class: re-check the event bits AFTER
//     you acquire motorMutex, in case the world changed while you were
//     waiting for the mutex.
// ---------------------------------------------------------------------------
void vMotionTask(void *pvParameters) {
  UART_sendString("Motion");
  (void)pvParameters;
  Packet packet = {0, 0, 0};
  TickType_t lastWake = xTaskGetTickCount();

  while (1) {
    // TODO: check EVENT_COMMS_OK / EVENT_COLLISION.
    // TODO: copy latestPacket under packetMutex.
    // TODO: under motorMutex, call lineFollowDrive(...) or stopMotors().

    vTaskDelayUntil(&lastWake, 1);
  }
}

// ---------------------------------------------------------------------------
// TODO 3/5: vCollisionTask -- override everything on a bump.
//
// Goal: if either collision sensor fires, set EVENT_COLLISION, take
// motorMutex, call performUTurn(), then clear EVENT_COLLISION.
//
// Hints:
//   - collision_65.isCollision() || collision_66.isCollision()
//   - This task will run at a HIGHER priority than the others (you'll set
//     that in setup(), TODO 5) so it can preempt line-following immediately.
// ---------------------------------------------------------------------------
void vCollisionTask(void *pvParameters) {
  UART_sendString("Collision");
  (void)pvParameters;
  TickType_t lastWake = xTaskGetTickCount();

  while (1) {
    // TODO: check both collision sensors.
    // TODO: set EVENT_COLLISION, take motorMutex, performUTurn(), give motorMutex, clear EVENT_COLLISION.

    vTaskDelayUntil(&lastWake, 1);
  }
}

// ======================= Setup and loop ===========================================

void setup() {
  UART_init();
  UART_sendString("Setup");

  setupTimer3_1ms();
  stopMotors();

  packetMutex = xSemaphoreCreateMutex();
  motorMutex = xSemaphoreCreateMutex();
  systemEvents = xEventGroupCreate();

  if (packetMutex == NULL || motorMutex == NULL || systemEvents == NULL) {
    stopMotors();
    while (1) {
    }
  }

  rgbled_67.fillPixelsBak(0, 2, 1);
  rgbled_68.fillPixelsBak(0, 2, 1);

  TCCR1A = _BV(WGM10);
  TCCR1B = _BV(CS11) | _BV(WGM12);

  TCCR2A = _BV(WGM21) | _BV(WGM20);
  TCCR2B = _BV(CS21);

  rgbled_67.setColor(0, 0, 0, 0);
  rgbled_67.show();
  rgbled_68.setColor(0, 0, 0, 0);
  rgbled_68.show();

  xEventGroupClearBits(systemEvents, EVENT_COMMS_OK);
  markPacketReceived();

  // ---------------------------------------------------------------------
  // TODO 4/5: create the three tasks you just wrote.
  //
  // Follow the pattern of the two already here:
  //   xTaskCreate(<function>, "<name>", <stack words>, NULL, <priority>, NULL)
  //
  // TODO 5/5: pick priorities.
  //   - vCollisionTask should be priority 2 (higher) so a bump preempts
  //     everything else immediately.
  //   - Everything else (UART, Safety, Motion, LED) can be priority 1.
  //   - 256 stack words is a safe default for most of these tasks; vLEDTask
  //     can get by with less (192) since it does very little per loop.
  // ---------------------------------------------------------------------
  bool tasksCreated =
      xTaskCreate(vUARTTask, "UART", 256, NULL, 1, NULL) == pdPASS
      && xTaskCreate(vLEDTask, "LED", 192, NULL, 1, NULL) == pdPASS;
      // TODO: && xTaskCreate(vSafetyTask, "Safety", 256, NULL, ?, NULL) == pdPASS
      // TODO: && xTaskCreate(vMotionTask, "Motion", 256, NULL, ?, NULL) == pdPASS
      // TODO: && xTaskCreate(vCollisionTask, "Collision", 256, NULL, ?, NULL) == pdPASS

  if (!tasksCreated) {
    UART_sendString("failed");
    stopMotors();
    while (1) {
    }
  }

  vTaskStartScheduler();

  // Should be unreachable on a correctly configured board.
  stopMotors();
  UART_sendString("scheduler failed to start");
  while (1) {
  }
}

void loop() {
  // Intentionally empty: FreeRTOS owns the CPU after vTaskStartScheduler().
}
