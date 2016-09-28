#!/usr/bin/python
import sys
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
from threading import Thread
import paho.mqtt.client as mqtt 
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
light = GPIO.LOW
sleepTime = 5
buzPitch = 5000

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
    buz(buzPitch,0.05*dist)
    time.sleep(0.05*dist)
    buzzerEnd=time.time()

def alert(var):
  while (secure==2):
    buz(buzPitch,0.25)
    time.sleep(0.1)

def on_connect(client, userdata, flags, rc): 
  print("Connected with result code "+str(rc)) 
  client.subscribe("topic/test") 

def on_message(client, userdata, msg): 
  global secure
  print(msg.payload)
  if(msg.payload=="0"):
    secure=0
  elif(msg.payload=="1"):
    secure=1
  elif(msg.payload=="2"):
    secure=0

def connect():
  client = mqtt.Client() 
  client.connect("localhost",1883,60) 

  client.on_connect = on_connect 
  client.on_message = on_message 

  client.loop_forever()

t = Thread(target=connect)
t.start()

while True: 
  print secure
  if secure == 0:
    if (prevSecure == 1):
      light=GPIO.HIGH
      GPIO.output(LIGHT_PIN, light)
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
      t = Thread(target=myfunc, args=(distance,))
      t.start()
    if (distance > 50 and light == GPIO.HIGH):
      light=GPIO.LOW
      GPIO.output(LIGHT_PIN, light)
    elif (distance < 50 and light == GPIO.LOW):
      light=GPIO.HIGH
      GPIO.output(LIGHT_PIN, light)
    print "Distance : ",distance,"cm"
    prevSecure=0

  elif (secure==1):
    if (prevSecure == 0):
      light=GPIO.LOW
      GPIO.output(LIGHT_PIN, light)

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

    if (distance>10):
      secure=2
      light=GPIO.HIGH
      GPIO.output(LIGHT_PIN, light)
      #takephoto
      alert(20)
  elif (secure==2):
    print "danger"
  #temperature part
  humidity, temperature = Adafruit_DHT.read_retry(sensor, TEMPERATURE_PIN) 
  if humidity is not None and temperature is not None: 
    print 'Temp : {0:0.1f}*C '.format(temperature)
    print temperature 
    print 'Humidity : {0:0.1f}% '.format(humidity)
  else: 
    print 'Failed to get reading. Try again!'

  print"######################"
GPIO.cleanup()
