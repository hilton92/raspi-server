
# Author: Ben Hilton
# Date: April 2022
# Humidity Control

import RPi.GPIO as GPIO
import time
import board
import adafruit_ahtx0


fanRelayPin = 11 
pumpRelayPin = 13 

setHumidity = 45
overrideStartTime = 0

i2c = board.I2C()
sensor = adafruit_ahtx0.AHTx0(i2c)

GPIO.setup(fanRelayPin, GPIO.OUT)
GPIO.setup(pumpRelayPin, GPIO.OUT)


def measure_humidity():
	return sensor.relative_humidity
	
def measure_temperature():
	return (sensor.temperature * 9/5) + 32

def report_humidity(thisHumidity):
	with open('data.txt', 'r') as file:
		data = file.readlines()
		data[0] = str(int(thisHumidity)) + "\n"	

	with open('data.txt', 'w') as file:
		file.writelines(data)

def report_temperature(thisTemperature):
	with open('data.txt', 'r') as file:
		data = file.readlines()
		data[1] = str(int(thisTemperature)) + "\n"	

	with open('data.txt', 'w') as file:
		file.writelines(data)
		
def get_fan_status():
	with open('data.txt', 'r') as file:
		return str(file.readlines()[2])
		
def get_pump_status():
	with open('data.txt', 'r') as file:
		return str(file.readlines()[3])
		
def get_override_status():
	with open('data.txt', 'r') as file:
		return file.readlines()[4]

def set_override_status(indicator):
	with open('data.txt', 'r') as file:
		data = file.readlines()
		data[4] = str(indicator)	

	with open('data.txt', 'w') as file:
		file.writelines(data)
		
def set_fan_status(thisString):
	with open('data.txt', 'r') as file:
		data = file.readlines()
		data[2] = str(thisString)	

	with open('data.txt', 'w') as file:
		file.writelines(data)

def set_pump_status(thisString):
	with open('data.txt', 'r') as file:
		data = file.readlines()
		data[3] = str(thisString)	

	with open('data.txt', 'w') as file:
		file.writelines(data)
		
def turn_on_fan():
	GPIO.output(fanRelayPin, 0)
	set_fan_status("on")

def turn_on_pump():	
	GPIO.output(pumpRelayPin, 0)  #turn on pump by setting low
	set_pump_status("on")
	
def turn_off_fan():
	GPIO.output(fanRelayPin, 1) #turn off fan by setting high
	set_fan_status("off")
	
def turn_off_pump():
	GPIO.output(pumpRelayPin, 1) #turn off pump by setting high
	set_pump_status("off")
	
def override_time_elapsed():
	if overrideStartTime == 0:
		#hasn't been started yet
		overrideStartTime = time.time()
		return false
	elif (overrideStartTime - time.time()) > 1800:
		overrideStartTime = 0
		return True
	else:
		return False


if __name__ == '__main__':
	try:
		while True:
			if (get_override_status == "1"):
				if (override_time_elapsed()):
					set_override_status("0")
					
			else:
				if measure_humidity() < setHumidity:
					turn_on_fan()
			time.sleep(5) #sleep for 5 seconds
			report_humidity(measure_humidity())
			report_temperature(measure_temperature())		
			
	finally:
		GPIO.cleanup()
