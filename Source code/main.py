## Speed fan controller design based on Fuzzy Logic using presence, temperature, and humidity sensors and ESP32 microcontroller.
## Programme for ESP32 microcontroller
## File main.py
## print built-in function is used along the programme to monitorise the lines on console
## script ver 3.4 - 05/08/2022
## Created by Ivan Fernandez Alonso

##  Imports the necessary modules from MicroPython library

import BME280                   # Note the module BME280 has been modified and only provides integer values with two decimal places
import ssd1306                  # module for OLED display with the ssd1306 chip CMOS
import time
import fuzzylogic               # module for fuzzy logic
from time import sleep
from machine import Timer
from machine import Pin
from machine import PWM
from machine import SoftI2C    


#  ESP32 - Pin assignments

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))        
detection = Pin(19, Pin.IN)                        
bme = BME280.BME280(i2c=i2c)                      
pin_led = Pin(32, Pin.OUT)                          
pwm33 = PWM(Pin(33))                              
pwm33.freq(1000)                                  
pwm33.duty(0)                                      


#  OLED DISPLAY start

oled_width = 128                                         
oled_height = 32                                        
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

oled.text('ESP32 MCU', 28, 5)
oled.text('______________________________', 0, 10)
oled.text('FUZZY LOGIC', 22, 25)                        # only for 64 oled height
oled.text('SPEED CONTROLLER', 0, 40)
oled.text('FAN EXTRACTOR', 14, 55)
oled.show()
time.sleep(4)
oled.fill(0)
oled.text('Waiting for', 20, 20)
oled.text('DATA', 45, 35)
oled.show()
time.sleep(1)

service_light = 'OFF'            
service_fan = 'OFF'                
temp_str = '0'                     
hum_str = '0'                    
pwm_str = '0'                      


#  MAIN FUNCTIONS

def sensor_bme():                     

    i = 1

    global temp, hum, temp_str, hum_str    

    while i <= 1:

        temp = int(float(bme.temperature)) 
        temp_str = str(int(float(temp)))
        hum = int(float(bme.humidity))
        hum_str = str(int(float(hum)))
        print('Temperature: ', temp)        
        print('Humidity: ', hum)            
        i = i + 1


def sensor_presence():

    i = 1

    global presence

    while i <= 1:

        presence = int(detection.value())       
                                               
        print('Motion detection :', presence)   
        i = i + 1


def data_display():

    i = 1

    while i <= 1:
        oled.fill(0)                            
        oled.text('[Temp][Hum][PWM]', 0, 3)
        oled.text(temp_str, 8, 17)            
        oled.text('C', 28, 17)
        oled.text(hum_str, 52, 17)             
        oled.text('%', 72, 17)
        oled.text(pwm_str, 95, 17)                 
        oled.text('__________________', 0, 24)
        oled.text('Light status ', 2, 39)
        oled.text('Fan status ', 20, 56)
        oled.text(service_light, 105, 39)       
        oled.text(service_fan, 105, 56)         
        oled.show()
        i = i + 1


def control_light():

    global service_light

    if presence == 1:
        pin_led.on()                         # set pin32 high level if presence is detected high level
        timer = Timer(0)                 
        timer.init(period=30000, mode=Timer.ONE_SHOT, callback=lambda t:light_status())
        service_light = 'ON'              
        print('Light is ON')

    elif presence == 0:

        print('Ligth is OFF')


def light_status():

    global service_light     

    pin_led.off()           
    service_light = 'OFF'
    print('Ligth is OFF')


def control_fan():

    global pwm

    ## passes the sensor temperature, sensor humidity and presence value to fuzzylogic_40 module

    fuzzylogic.init(temp, hum, presence)

    ## return the final duty cycle percentage into value object

    pwm = fuzzylogic.crisp_output()

    print('Fan value pwm: ', pwm)      


def fan_service():

    global service_fan, pwm_str
    pwm_str = str(pwm)

    if pwm >= 20:
        pwm33.duty(pwm)                     
        timer = Timer(1)                    
        timer.init(period=60000, mode=Timer.ONE_SHOT, callback=lambda t:fan_status())   
        service_fan = 'ON'
        print('FAN is ON')

    else:
        print('FAN is OFF')


def fan_status():

    global service_fan

    pwm33.duty(0)                
    service_fan = 'OFF'
    print('FAN is OFF')


while True:                                    

    sensor_bme()
    sensor_presence()
    data_display()
    control_light()
    control_fan()
    fan_service()
    print('CONTROL PROCESS COMPLETED', '\n', '\n')
    time.sleep_ms(500)                       
