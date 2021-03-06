import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

buzzerPin = 21
GPIO.setup(buzzerPin, GPIO.OUT) # PWM pin set as output
waktu=0.0001
def buz(pitch,duration):
        period = 1.0/pitch
        delay = period /2
        cycles = int (duration*pitch)
        for i in range(cycles):
                GPIO.output(buzzerPin, True)
                time.sleep(delay)
                GPIO.output(buzzerPin, False)
                time.sleep(delay)

interval=sys.argv
start = time.time()
end = time.time()
while (end - start < 1):
	startInterval = time.time()
        endInterval = time.time()
        while (endInterval-start interval < interval):
                buz(5000,7)
        time.sleep(interval)
        end = time.time()

GPIO.cleanup() # cleanup all GPIO
