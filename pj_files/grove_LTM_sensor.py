
#!/usr/bin/env python
#
# GrovePi Example for using the Grove Light Sensor and the LED together to turn the LED On and OFF if the background light is greater than a threshold.
# Modules:
# 	http://www.seeedstudio.com/wiki/Grove_-_Light_Sensor
# 	http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit

# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import time
import grovepi
import sys
import paho.mqtt.client as mqtt
import json
import os 

SERVER = '172.16.103.156'

INTERVAL=3

next_reading = time.time()

client = mqtt.Client("P1")

client.connect(SERVER,1883,60)

client.loop_start()

# SIG,NC,VCC,GND
light_sensor = 0
temp_sensor= 1
# Connect the LED to digital port D4
# SIG,NC,VCC,GND
led = 4

#motion sensor 
pir_sensor=8
motion=0
grovepi.pinMode(pir_sensor,"INPUT")
 
# Turn on LED once sensor exceeds threshold resistance
threshold = 10

grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(led,"OUTPUT")


#f = open("demofile2.txt", "a")
while True:
    try:
        # Get Light sensor value
        sensor_value = grovepi.analogRead(light_sensor)
	if sensor_value == 0:
		sensor_value = 1
       
        #Get Temerature Value
        temp= grovepi.temp(temp_sensor,'1.1')
       
        #Get Motion Sensor Value  
        motion=grovepi.digitalRead(pir_sensor) 
       
        #Calculate resistance of sensor in K
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value

        if resistance > threshold:
            # Send HIGH to switch on LED
            grovepi.digitalWrite(led,1)
        else:
            # Send LOW to switch off LED
            grovepi.digitalWrite(led,0)

        #f.write("sensor_value = %d\n" %(sensor_value)) 
        #print("sensor_value = %d %(sensor_value))
        print("sensor_value = %d resistance = %.2f" %(sensor_value,  resistance))
        print("temperature=%d" %(temp))
        print("Motion=%d" %(motion)) 
       
        client.publish('ras_2/lab_1/light',json.dumps(sensor_value))
        client.publish('ras_2/lab_1/temperature',json.dumps(temp))
        client.publish('ras_2/lab_1/motion_sensor',json.dumps(motion))

        next_reading += INTERVAL 
        sleep_time =next_reading-time.time()
        if sleep_time >0:
            time.sleep(sleep_time) 
    except IOError:
        f.close() 


client.loop_stop()
client.disconnect()
