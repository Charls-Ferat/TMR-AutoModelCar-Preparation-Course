# src/ — put your MegaPi hardware files here

This sketch expects two files in this exact folder:

```
src/MeNewRGBLed.h
src/MeNewRGBLed.cpp
src/MeCollisionSensor.h
src/MeCollisionSensor.cpp
```

These are your own Makeblock MegaPi RGB LED and collision-sensor wrapper
classes — copy them from your existing MBot project into this folder.
They are not provided here because they're specific to your hardware
revision/wiring, not to the FreeRTOS/software side this course teaches.

The sketch will not compile until these four files are present.
