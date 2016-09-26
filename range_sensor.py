import RPi.GPIO as GPIO
import sys
import time
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 4
update_0 = 0
update_1 = 0
GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24

print "Distance Measurement In Progress"


while True: 
  GPIO.setup(TRIG,GPIO.OUT)
  GPIO.setup(ECHO,GPIO.IN)

  GPIO.output(TRIG, False)
  print "Waiting For Sensor To Settle"
  time.sleep(1)

  GPIO.output(TRIG, True)

  time.sleep(0.00001)
  GPIO.output(TRIG, False)

  while GPIO.input(ECHO)==0:
    pulse_start = time.time()

  while GPIO.input(ECHO)==1:
    pulse_end = time.time()

  pulse_duration = pulse_end - pulse_start

  distance = pulse_duration * 17150

  distance = round(distance, 2)

  print "Distance:",distance,"cm"

GPIO.cleanup()
