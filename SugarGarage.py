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
LIGHT_PIN = 20
RANGE_TRIG = 23 
RANGE_ECHO = 24

GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LIGHT_PIN, GPIO.OUT)
GPIO.setup(RANGE_TRIG,GPIO.OUT)
GPIO.setup(RANGE_ECHO,GPIO.IN)
sensor = Adafruit_DHT.DHT11

secure = 0
prevSecure = 0
light = 0
sleepTime = 5

def buz(pitch,duration):
  period = 1.0/pitch
  delay = period /2
  cycles = int (duration*pitch)
  for i in range(cycles):
    GPIO.output(BUZZER_PIN, True)
    time.sleep(delay)
    GPIO.output(BUZZER_PIN, False)
    time.sleep(delay)
def myfunc(dist):
  dist=dist-2
  buzzerStart=time.time()
  buzzerEnd=time.time()
  while (buzzerEnd-buzzerStart<sleepTime):
    buz(50,0.05*dist)
    time.sleep(0.05*dist)
    buzzerEnd=time.time()

GPIO.output(LIGHT_PIN, True)

while True: 
  if secure == 0:
    #if (prevSecure == 1):
      #lightOn
    #distance part 
    GPIO.output(RANGE_TRIG, False)
    #print "Waiting For Sensor To Settle"
    time.sleep(sleepTime)

    GPIO.output(RANGE_TRIG, True)

    time.sleep(0.00001)
    GPIO.output(RANGE_TRIG, False)

    while GPIO.input(RANGE_ECHO)==0:
      pulse_start = time.time()

    while GPIO.input(RANGE_ECHO)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance)

    if (distance<20):
      print "Distance Urgent : ",distance,"cm",x
      t = Thread(target=myfunc, args=(distance,))
      t.start()
    else:
      print "Distance : ",distance,"cm",x
    prevSecure=0

  elif (secure==1):
    print "Secure"
  #temperature part
  humidity, temperature = Adafruit_DHT.read_retry(sensor, TEMPERATURE_PIN) 
  if humidity is not None and temperature is not None: 
    print 'Temp : {0:0.1f}*C '.format(temperature) 
    print 'Humidity : {0:0.1f}% '.format(humidity)
  else: 
    print 'Failed to get reading. Try again!'

  print"######################"
GPIO.cleanup()
