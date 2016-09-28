#!/usr/bin/env python 

import paho.mqtt.client as mqtt 
import time
from threading import Thread

# This is the Subscriber 

def on_connect(client, userdata, flags, rc): 
	print("Connected with result code "+str(rc)) 
	client.subscribe("topic/test") 

def on_message(client, userdata, msg): 
	print(msg.payload) 


def myfunc(i):
	client = mqtt.Client() 
	client.connect("localhost",1883,60) 

	client.on_connect = on_connect 
	client.on_message = on_message 

	client.loop_forever()

i=10
t = Thread(target=myfunc, args=(i,))
t.start()

print "hai"