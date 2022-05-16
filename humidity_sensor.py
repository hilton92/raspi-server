# Author: Ben Hilton
# Date: April 2022
# Humidity Control

import RPi.GPIO as GPIO
from flask import Flask, render_template
import time
import board
import adafruit_ahtx0
import csv

app = Flask(__name__)


fanRelayPin = 11 
pumpRelayPin = 13 
fanOn = False
pumpOn = False
overRide = False
currentHumidity = 45
currentTemperature = 120
setHumidity = 45

#i2c = board.I2C()
#sensor = adafruit_ahtx0.AHTx0(i2c)

GPIO.setup(fanRelayPin, GPIO.OUT)
GPIO.setup(pumpRelayPin, GPIO.OUT)


@app.route('/')
def index():
	templateData = {
		'title' : 'Humidity Sensor', 
		'isFanOn' : fanOn,
		'isPumpOn' : pumpOn,
		'humidityLevel' : currentHumidity}
	return render_template('index.html', **templateData)

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	overRide = True
	if deviceName == 'fan' and action == "on":
		turn_on_fan()
	if deviceName == 'fan' and action == "off":
		turn_off_fan()
	if deviceName == 'pump' and action == "on":
		turn_on_pump()
	if deviceName == 'pump' and action == "off":
		turn_off_pump()
	templateData = {
		'isFanOn' : fanOn,
		'isPumpOn' : pumpOn,
		'humidityLevel' : currentHumidity}
	return render_template('index.html', **templateData)

def get_humidity():
	with open('data.txt', 'r') as file:
	return file.readlines()[0]

def get_temperature():
	with open('data.txt', 'r') as file:
	return file.readlines()[1]

def turn_on_fan():
	with open('data.txt', 'r') as file:
	data = file.readlines()
	data[2] = '1\n'	

	with open('data.txt', 'w') as file:
	file.writelines(data)	

	fanOn = True
	print("Turning on fan")

def turn_on_pump():	
	GPIO.output(pumpRelayPin, 0)  #turn on pump by setting low
	pumpOn = True
	print("Turning on pump")
def turn_off_fan():
	GPIO.output(fanRelayPin, 1) #turn off fan by setting high
	fanOn = False
	print("Turning off fan")
def turn_off_pump():
	GPIO.output(pumpRelayPin, 1) #turn off pump by setting high
	pumpOn = False
	print("Turning off pump")


if __name__ == '__main__':
	try:
		app.run(debug = True,threaded=True, port = 80, host = '0.0.0.0')
	finally:
		GPIO.cleanup()

