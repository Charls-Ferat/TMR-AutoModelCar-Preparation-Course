# Week 5 — Robotics: MBot MegaPi + FreeRTOS

## Learning goals
- Read and extend a real multi-task FreeRTOS program: tasks, mutexes,
  event groups, priorities.
- Understand a framed UART protocol with a checksum, and why that's more
  robust than "just read bytes".
- Build the task graph that turns a host computer's steering commands
  into actual motor output on the MBot MegaPi, safely.
- Drive the car with the exact steering model trained in
  Week 3/4, closing the loop from the whole course.

## Folder layout

```text
week5_robotics_mbot/
├── README.md                              
├── student_mbot_toolbox/                  
│   ├── student_mbot_toolbox.ino
│   └── src/                               <- sensor and movement grappers
└── host_side/                             <- optional: laptop -> MBot over serial
    ├── mbot_serial.py
    ├── live_steering_demo.py
    └── requirements.txt
```

## Connecting back to the rest of the course 

`host_side/` is a small, optional add-on showing how a laptop running
the exact steering CNN from Week 3/4 can drive this car for real:

```bash
cd week5_robotics_mbot/host_side
pip install -r requirements.txt
python3 live_steering_demo.py --model ../../week3_steering_model/data/steering_cnn.pt --port /dev/ttyUSB0
```

## Safety notes
- Always test with wheels off the ground before a floor/track test.
- Keep a hand near the power switch during the first few runs of any
  new TODO implementation.
- The watchdog (`vSafetyTask`) only protects against *lost comms* — a
  bad model prediction that's still arriving on time will still be
  obeyed. Keep speeds low while validating a new model on real hardware.
