#!/usr/bin/python
import sys
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
from threading import Thread
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TEMPERATURE_PIN = 4
BUZZER_PIN = 21
RANGE_TRIG = 23 
RANGE_ECHO = 24

GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.setup(RANGE_TRIG,GPIO.OUT)
GPIO.setup(RANGE_ECHO,GPIO.IN)
sensor = Adafruit_DHT.DHT11

def buz(pitch,duration):
        period = 1.0/pitch
        delay = period /2
        cycles = int (duration*pitch)
        for i in range(cycles):
                GPIO.output(buzzerPin, True)
                time.sleep(delay)
                GPIO.output(buzzerPin, False)
                time.sleep(delay)

secure = 1

while True: 
  if secure == 1:
    for x in xrange(0, 5):
       #distance part 
      GPIO.output(RANGE_TRIG, False)
      #print "Waiting For Sensor To Settle"
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

      if (distance<10):
        print "Distance Urgent : ",distance,"cm",x

      else:
        print "Distance : ",distance,"cm",x
  else:
  #temperature part
  humidity, temperature = Adafruit_DHT.read_retry(sensor, TEMPERATURE_PIN) 
  if humidity is not None and temperature is not None: 
    print 'Temp : {0:0.1f}*C '.format(temperature) 
    print 'Humidity : {0:0.1f}% '.format(humidity)
  else: 
    print 'Failed to get reading. Try again!'

  print"######################"
GPIO.cleanup()
