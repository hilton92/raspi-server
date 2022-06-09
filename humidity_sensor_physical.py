
# Author: Ben Hilton
# Date: April 2022
# Humidity Control

import RPi.GPIO as GPIO
import time
from datetime import date
from datetime import datetime
from csv import writer
import board
import adafruit_ahtx0

today = date.today()
todaysDate = today.strftime("%b-%d-%Y")

#pins for pump and fan relays
fanRelayPin = 11 
pumpRelayPin = 13 

setHumidity = 45 # desired humidity of room

#timer variables - when fan or pump status is overridden, it remains overridden for 30 minutes
#when the ideal humidity is reached, pump turns off but fan stays on for 10 minutes
overrideStartTime = 0
fanOnStartTime = 0

# I2C variables
i2c = board.I2C()
sensor = adafruit_ahtx0.AHTx0(i2c)

#setup fan and pump relay pins as outputs
GPIO.setup(fanRelayPin, GPIO.OUT)
GPIO.setup(pumpRelayPin, GPIO.OUT)

#measure the humidity from AHTx0 sensor
def measure_humidity():
	return sensor.relative_humidity

#measure the temperature from AHTx0 sensor (and convert to F)	
def measure_temperature():
	return (sensor.temperature * 9/5) + 32 #convert C to F

#update the shared text file with the humidity so it can be read by webpage
def report_humidity(thisHumidity):
	with open('data.txt', 'r') as file:
		data = file.readlines()
		data[0] = str(int(thisHumidity)) + "\n"	

	with open('data.txt', 'w') as file:
		file.writelines(data)

#update the shared text file with the temperature so it can be read by webpage
def report_temperature(thisTemperature):
	with open('data.txt', 'r') as file:
		data = file.readlines()
		data[1] = str(int(thisTemperature)) + "\n"	

	with open('data.txt', 'w') as file:
		file.writelines(data)
		
#read shared text file to get fan status		
def get_fan_status():
	with open('data.txt', 'r') as file:
		return str(file.readlines()[2])
		
#read shared text file to get pump status		
def get_pump_status():
	with open('data.txt', 'r') as file:
		return str(file.readlines()[3])
		
#read shared text file to get override status		
def get_override_status():
	with open('data.txt', 'r') as file:
		return str(file.readlines()[4])

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
	GPIO.output(fanRelayPin, 0) # turn on fan by setting low
	set_fan_status("on\n")
	print("Turning on fan")

def turn_on_pump():	
	GPIO.output(pumpRelayPin, 0)  #turn on pump by setting low
	set_pump_status("on\n")
	print("Turning on pump")
	
def turn_off_fan():
	GPIO.output(fanRelayPin, 1) #turn off fan by setting high
	set_fan_status("off\n")
	print("Turning off fan")
	
def turn_off_pump():
	GPIO.output(pumpRelayPin, 1) #turn off pump by setting high
	set_pump_status("off\n")
	print("Turning off pump")
	
def override_time_elapsed():
	global overrideStartTime
	if overrideStartTime == 0:
		#hasn't been started yet
		overrideStartTime = time.time()
		return False
	elif (time.time() - overrideStartTime) > 1800:
		overrideStartTime = 0
		return True
	else:
		return False

def start_fan_timer():
	global fanOnStartTime
	if fanOnStartTime == 0:
		#hasn't been started yet
		fanOnStartTime = time.time()

def fan_time_elapsed():
	global fanOnStartTime
	if (time.time() - fanOnStartTime) > 600:
		fanOnStartTime = 0
		return True
	else:
		return False

def reset_shared_file():
	data = ["20\n", "20\n", "off\n", "off\n", "no"]
	with open('data.txt', 'w') as file:
		file.writelines(data)

if __name__ == '__main__':
	try:
		reset_shared_file()
		while True:
			for i in range(6):	
				if (get_override_status() == "yes"):
					if (override_time_elapsed()):
						set_override_status("no")
					if get_fan_status() == "on\n":
						turn_on_fan()
					if get_fan_status() == "off\n":
						turn_off_fan()
					if get_pump_status() == "on\n":
						turn_on_pump()
					if get_pump_status() == "off\n":
						turn_off_pump()	
				else:
					if measure_humidity() < setHumidity - 5:
						turn_on_fan()
						turn_on_pump()
					if measure_humidity() > setHumidity:
						turn_off_pump()	
						start_fan_timer()
						if fan_time_elapsed():
							turn_off_fan()
						
				time.sleep(5) #sleep for 5 seconds
				report_humidity(measure_humidity())
				report_temperature(measure_temperature())
				
			#write to file (once every 30 seconds)
			now = datetime.now()
			currentTime = now.strftime("%H-%M-%S")
			writeData = [currentTime, int(measure_humidity()), int(measure_temperature())]	
			with open('/home/ras-pi-user/humidifier_data/' + todaysDate + '.csv', 'a', newline='') as fileObject:
				writerObject = writer(fileObject)
				writerObject.writerow(writeData)
				fileObject.close()
	finally:
		GPIO.cleanup()
