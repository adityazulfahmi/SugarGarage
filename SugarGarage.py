#!/usr/bin/python
import sys
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

RANGE_TRIG = 23 
RANGE_ECHO = 24
sensor = Adafruit_DHT.DHT11
TEMPERATURE_PIN = 4
update_0 = 0
update_1 = 0
GPIO.setup(RANGE_TRIG,GPIO.OUT)
GPIO.setup(RANGE_ECHO,GPIO.IN)

while True: 
  
  GPIO.output(RANGE_TRIG, False)
  print "Waiting For Sensor To Settle"
  time.sleep(1)

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

  print "Distance:",distance,"cm"

GPIO.cleanup()
