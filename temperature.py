#!/usr/bin/python
import sys
import time
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 4
update_0 = 0
update_1 = 0

while True:
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin) 
	update_0 = temperature
	update_1 = humidity
	if humidity is not None and temperature is not None: 
		print 'Temp = {0:0.1f}*C '.format(temperature) 
		print 'Humidity = {0:0.1f}% '.format(humidity) 
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin) 
		time.sleep(1)

	else: 
		print 'Failed to get reading. Try again!'

	if update_0 != temperature : 
		print"##### UPDATE ! ! ! #####"

	if update_1 != humidity : 
		print"##### UPDATE ! ! ! #####"

	else: 
		print"######################"
