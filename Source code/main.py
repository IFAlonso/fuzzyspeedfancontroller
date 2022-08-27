## Speed fan controller design based on Fuzzy Logic using presence, temperature, and humidity sensors and ESP32 microcontroller.
## Programme for ESP32 microcontroller
## File main.py
## print built-in function is used along the programme to monitorise the lines on console
## script ver 3.1 - 22/07/2022
## Created by Ivan Fernandez Alonso
## Electronics Engineering.

##  Imports the necessary modules

import BME280                   # module for temperature and humidity sensor BME280
## Note the module BME280 has been modified and only provides integer values with two decimal places
import ssd1306                  # module for OLED display with the ssd1306 chip CMOS
import time
import fuzzylogic               # module for fuzzy logic
from time import sleep
from machine import Timer
from machine import Pin
from machine import PWM
from machine import SoftI2C     # module for the I2C bus communication



#  ESP32 - Pin assignments

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))             # object for i2c bus
detection = Pin(19, Pin.IN)                         # object input pin on GPIO19 for presence sensor
bme = BME280.BME280(i2c=i2c)                        # object for temp & hum sensor
pin25 = Pin(25, Pin.OUT)                            # create output pin on GPIO25 for light output
pwm33 = PWM(Pin(33))                                # create PWM object on GPIO33
pwm33.freq(10000)                                   # set PWM frequency MHz
pwm33.duty(0)                                       # sets the initial value for PWM duty cycle


#  OLED DISPLAY 0.91 inch start

oled_width = 128                                            # sets width of the oled display
oled_height = 64                                            # sets height of the oled display
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.text('ESP32 MCU', 28, 5)
oled.text('______________________________', 0, 10)
oled.text('FUZZY LOGIC', 22, 25)
oled.text('SPEED CONTROLLER', 0, 40)
oled.text('FAN EXTRACTOR', 14, 55)
oled.show()
time.sleep(5)
oled.fill(0)
oled.text('Waiting for', 20, 20)
oled.text('DATA', 45, 35)
oled.show()
time.sleep(1)

service_light = 'OFF'               # by default light status is OFF
service_fan = 'OFF'                 # by default fan status is OFF
temp_str = '0'                      # by default temperature value shown on OLED display is zero
hum_str = '0'                       # by default humidity value shown on OLED display is zero
pwm_str = '0'                       # by default PWM value shown on OLED display is zero


#  MAIN FUNCTIONS

def sensor_bme():                       # funcion for the sensor BME280 temperature and humidity

    i = 1

    global temp, hum, temp_str, hum_str     # creates global objects

    while i <= 1:

        temp = int(float(bme.temperature))  # obtain value from BME sensor and converts into integer
        temp_str = str(int(float(temp)))
        hum = int(float(bme.humidity))
        hum_str = str(int(float(hum)))
        print('Temperature: ', temp)        # just for control purposes on console
        print('Humidity: ', hum)            # just for control purposes on console
        i = i + 1



def sensor_presence():

    i = 1

    global presence

    while i <= 1:

        presence = int(detection.value())       # it obtains a high state (detection) or low state (no presence)
                                                # and pass the value into the presence object
        print('Motion detection :', presence)   # just for control purposes on console
        i = i + 1



def data_display():

    i = 1

    while i <= 1:
        oled.fill(0)                            # cleans the OLED display
        oled.text('[Temp][Hum][PWM]', 0, 3)
        oled.text(temp_str, 8, 17)             # it updates the temperature value on OLED display
        oled.text('C', 28, 17)
        oled.text(hum_str, 52, 17)              # it updates the humidity value on OLED display
        oled.text('%', 72, 17)
        oled.text(pwm_str, 95, 17)                 # it updates the PWM value on OLED display
        oled.text('__________________', 0, 24)
        oled.text('Light status ', 2, 39)
        oled.text('Fan status ', 20, 56)
        oled.text(service_light, 105, 39)       # it updates the light status on OLED display
        oled.text(service_fan, 105, 56)         # it updates the light status on OLED display
        oled.show()
        i = i + 1



def control_light():

    global service_light

    if presence == 1:
        pin25.on()                          # set pin25 high level if presence is detected high level
        timer = Timer(0)                    # Uses timer 0 for callback function light_status
        ## sets off delay for light 30 seconds when presence is not detected
        timer.init(period=30000, mode=Timer.ONE_SHOT, callback=lambda t:light_status())
        service_light = 'ON'                # it updates the object service_light for the OLED display
        print('Light is ON')

    elif presence == 0:

        print('Ligth is OFF')



def light_status():

    global service_light        # after 30s this function is called back and sets in low state the pin25.

    pin25.off()                 # Turn off the light
    service_light = 'OFF'
    print('Ligth is OFF')


def control_fan():

    global pwm

    ## passes the sensor temperature, sensor humidity and presence value to fuzzylogic_40 module

    fuzzylogic.init(temp, hum, presence)

    ## return the final duty cycle percentage into value object

    pwm = fuzzylogic.crisp_output()

    print('Fan value pwm: ', pwm)           # it shows the duty cycle value on console. Control purposes.


def fan_service():

    global service_fan, pwm_str
    pwm_str = str(pwm)

    if pwm >= 20:
        pwm33.duty(pwm)                         # passes the duty cycle value to GPIO 33. PWM output.
        timer = Timer(1)                        # it uses timer 1 for callback function fan_status
        timer.init(period=60000, mode=Timer.ONE_SHOT, callback=lambda t:fan_status())   # sets off delay for fan 60 seconds
        service_fan = 'ON'
        print('FAN is ON')

    else:
        print('FAN is OFF')



def fan_status():

    global service_fan

    pwm33.duty(0)                 # turn off PWM on the pin 33 after 60 if the fan variable is lower than 20
    service_fan = 'OFF'
    print('FAN is OFF')


while True:                                     # main loop for calling the functions inside the main.py

    sensor_bme()
    sensor_presence()
    data_display()
    control_light()
    control_fan()
    fan_service()
    print('CONTROL PROCESS COMPLETED', '\n', '\n')      # just for control purposes on console
    time.sleep_ms(500)                          # period of global processing. Every 0.5 senconds.
