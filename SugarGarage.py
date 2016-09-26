#!/usr/bin/python
import sys
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TEMPERATURE_PIN = 4
RANGE_TRIG = 23 
RANGE_ECHO = 24
GPIO.setup(RANGE_TRIG,GPIO.OUT)
GPIO.setup(RANGE_ECHO,GPIO.IN)
sensor = Adafruit_DHT.DHT11
update_0 = 0
update_1 = 0

while True: 
  #temperature part
  humidity, temperature = Adafruit_DHT.read_retry(sensor, TEMPERATURE_PIN) 
  update_0 = temperature
  update_1 = humidity
  if humidity is not None and temperature is not None: 
    print 'Temp : {0:0.1f}*C '.format(temperature) 
    print 'Humidity : {0:0.1f}% '.format(humidity) 
    humidity, temperature = Adafruit_DHT.read_retry(sensor, TEMPERATURE_PIN)

    #distance part 
    GPIO.output(RANGE_TRIG, False)
    #print "Waiting For Sensor To Settle"
    time.sleep(0.5)

    GPIO.output(RANGE_TRIG, True)

    time.sleep(0.00001)
    GPIO.output(RANGE_TRIG, False)

    while GPIO.input(RANGE_ECHO)==0:
      pulse_start = time.time()

    while GPIO.input(RANGE_ECHO)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    print "Distance : ",distance,"cm"
  else: 
    print 'Failed to get reading. Try again!'

  if update_0 != temperature : 
    print"##### UPDATE ! ! ! #####"

  if update_1 != humidity : 
    print"##### UPDATE ! ! ! #####"

  else: 
    print"######################"
GPIO.cleanup()
