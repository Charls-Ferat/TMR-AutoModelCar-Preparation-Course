"""
mbot_serial.py
----------------
Host-side (laptop) side of the UART protocol the MBot firmware expects:

    [SYNC][SPEED][STEER][FLAGS][CRC]   (5 bytes, 115200 baud)

    SYNC  = 0xAA (fixed)
    SPEED = uint8,  0-255
    STEER = int8,  -128..127  (car code maps roughly -40..40 to full lock)
    FLAGS = uint8, unused bits reserved for you
    CRC   = XOR of the first 4 bytes

This is the piece that lets your Week 3/4 steering CNN actually drive the
MBot: run the model on the laptop (or the car's own onboard computer if
it has one), turn its prediction into a (speed, steer) packet with
`build_packet`, and write it to the serial port the MBot is on.

Only dependency: pyserial (`pip install pyserial`). Nothing from
common/python is required here, but the steering model itself (Week 3/4)
is a drop-in: see `steering_prediction_to_packet` below.
"""

import time

SYNC_BYTE = 0xAA
PACKET_SIZE = 5


def _to_uint8(value: int) -> int:
    return max(0, min(255, int(value)))


def _to_int8(value: int) -> int:
    value = max(-128, min(127, int(value)))
    return value & 0xFF  # two's complement byte representation


def compute_crc(data: bytes) -> int:
    """Matches the firmware's computeCRC: XOR of all given bytes."""
    crc = 0
    for b in data:
        crc ^= b
    return crc


def build_packet(speed: int, steer: int, flags: int = 0) -> bytes:
    """
    Build one 5-byte packet matching the MBot firmware's expected format.

    speed : 0-255        (uint8 -- 0 = stopped)
    steer : -128..127    (int8  -- negative/positive = left/right;
                           the firmware's lineFollowDrive maps roughly
                           -40..40 to full correction, see its README)
    flags : 0-255        (uint8 -- reserved, send 0 unless you've added
                           your own meaning to specific bits in the firmware)
    """
    speed_byte = _to_uint8(speed)
    steer_byte = _to_int8(steer)
    flags_byte = _to_uint8(flags)

    body = bytes([SYNC_BYTE, speed_byte, steer_byte, flags_byte])
    crc = compute_crc(body)
    packet = body + bytes([crc])

    assert len(packet) == PACKET_SIZE
    return packet


def steering_prediction_to_packet(steering: float, base_speed: int = 150, flags: int = 0) -> bytes:
    """
    Convert a Week 3/4 steering-model prediction (a float roughly in
    [-1, 1]) into a packet the firmware understands.

    This is the one line that connects the whole course: `steering` here
    is exactly what `model(image_tensor).item()` returns in
    week3_steering_model/src/03_evaluate.py.
    """
    steer_byte = int(round(steering * 40))  # matches lineFollowDrive's -40..40 input range
    return build_packet(speed=base_speed, steer=steer_byte, flags=flags)


def send_forever(port: str, get_speed_and_steer, rate_hz: float = 20.0):
    """
    Open `port` and repeatedly call `get_speed_and_steer()` -- a function
    returning (speed, steer) -- sending one packet at `rate_hz`.

    Example:
        send_forever("/dev/ttyUSB0", lambda: (150, 0))   # drive straight
    """
    import serial  # imported here so the rest of this file works without pyserial installed

    period_s = 1.0 / rate_hz
    with serial.Serial(port, 115200, timeout=0) as ser:
        print(f"Connected to {port} at 115200 baud. Sending at {rate_hz} Hz. Ctrl+C to stop.")
        try:
            while True:
                speed, steer = get_speed_and_steer()
                ser.write(build_packet(speed, steer))
                time.sleep(period_s)
        except KeyboardInterrupt:
            print("\nStopping -- sending one final 'stop' packet.")
            ser.write(build_packet(speed=0, steer=0))


if __name__ == "__main__":
    # Minimal demo: drive straight at a constant speed.
    # Change the port to match your system:
    #   Linux/Mac: /dev/ttyUSB0 or /dev/ttyACM0
    #   Windows:   COM3 (check Device Manager)
    PORT = "/dev/ttyUSB0"
    send_forever(PORT, get_speed_and_steer=lambda: (150, 0), rate_hz=20.0)
