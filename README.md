This is the design of a control system to manage a fan speed using a BME280 temperature and humidity sensor along with the radar sensor RCWL-0516. This speed fan controller is based on fuzzy logic (Mamdani fuzzy inference method) to produce a PWM output signal provided by the ESP32 microcontroller unit. The fuzzy algorithm and MCU were programmed under the MicroPython language.
This control system can be implemented on any extractor fan that uses a power input between 12 V DC and 24 V DC. The most common applications are intended for bathrooms, but its application could be extended to kitchens, drying rooms, or any space where there is a need to control moisture levels with efficient power consumption.

Features:
- The power consumption of the extractor fan can be adapted to the real needs of the situation, which translates directly into an optimization of its energy costs.
- It has incorporated a digital output (high/low level) to control a light system by means of presence detection.

![PCB_prototype_frontview1](https://user-images.githubusercontent.com/95512993/189371198-46cae23d-2876-4beb-b871-ca7f631f24d3.jpg)


MEMBERSHIP FUNCTIONS

![image](https://user-images.githubusercontent.com/95512993/189966736-2222c179-b586-4f6c-8ce0-85e2768dcc1c.png)


