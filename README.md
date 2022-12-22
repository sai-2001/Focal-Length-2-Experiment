# FocalLength
***
Focal Length is a physics experiment, where the student can observe the sharp image at a
particular focal length as shown in the fig.55 by varying the screen and object distances.This
section consists of the physics behind the experiment, the software and hardware implementations of the experiment and it’s working.
***

## Project objectives

1.To provide web-based practical experience to students and allow them to perform
experiments over the internet.
2. To be able to provide an interactive user experience via the dashboard.
3. To calculate focal length of a biconvex lens by observing image formation by the
lens on an IoT enabled optical bench.

## Theory

The main physics behind the experiment can be summarized as:
To calculate the focal length of a lens you should be familiar with basic concepts of refraction of light from a lens and lens formula which will be used to calculate the focal length
by obtaining object and image distances with proper sign convention. The lens formula is
given by:
```1/f=1/v-1/u```

### Hardware Implementation
The hardware setup is built using hardwood and cardboard. A small part of the hardwood
has been removed from the middle end of the cardboard so that the stepper motors are
placed on it as shown in the fig.54. The stepper motor works based on the signals received
from A4988 motor drivers. 3D printed object and screen are attached to the rod and coupled
with the two stepper motors. The hardware setup is designed separately and merged as two
parts i.e. object and the screen part so that it can be easily removed when needed. The
lens holder is placed in between the two parts. The components are placed on the PCB
board and it is attached to the bottom part of the hardware setup to avoid uncertainty. The
raspberry pi cam is placed on the pan-tilt camera. The pan-tilt is designed in such a way
that it can be rotated in the horizontal direction to show the visuals of the object and screen
in the dashboard.
when the inputs are provided from the dashboard to turn on or leave the
experiment, the virtual buttons of the relay module in the blynk console turn on from 0 to
1 or 1 to 0 and the signals are provided to the raspberry pi. Then the raspberry pi provides
these high/Low signals to the relay which turns ON/OFF the LED Strip. When the User
provides inputs to change the direction of stepper motors to clockwise/anticlockwise, then
these inputs are provided to the raspberry pi from the blynk console and these signals are
received by the A4988 motor drivers which actuates the stepper motors which changes the
object/screen distance. The raspberry pi camera module captures the working and sends
action data to the raspberry pi which processes video data to YouTube live stream. Here, 12Volts DC supply is connected to the two motor drivers and the relay is connected to the raspberrypi which turns
on LED strip when signals are received from raspberry pi. Two A4988 motor drivers are
connected with the raspberrypi GPIO pins which inturn connects with the two NEMA17
stepper motors. The two limit switches are connected with the raspberry pi which is used
as a safety interlock, to limit the movement of object and screen passing a predetermined
point.
