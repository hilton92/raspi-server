# Author: Ben Hilton
# Date: April 2022
# Humidity Control

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
	thisHumidity = get_humidity()
	thisTemperature = get_temperature()
	thisFanStatus = get_fan_status()
	thisPumpStatus = get_pump_status()
	thisOverride = get_override_status()
	print("main loop:")
	templateData = {
		'title' : 'Humidity Sensor', 
		'isFanOn' : thisFanStatus,
		'isPumpOn' : thisPumpStatus,
		'humidityLevel' : thisHumidity,
		'temperature' : thisTemperature,
		'overridden' : thisOverride}
	return render_template('index.html', **templateData)

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
	set_override()
	thisHumidity = get_humidity()
	thisTemperature = get_temperature()
	thisOverride = get_override_status()
	if deviceName == 'fan' and action == "on":
		turn_on_fan()
		thisFanStatus = "on"
		thisPumpStatus = get_pump_status()
	elif deviceName == 'fan' and action == "off":
		turn_off_fan()
		thisFanStatus = "off"
		thisPumpStatus = get_pump_status()
	elif deviceName == 'pump' and action == "on":
		turn_on_pump()
		thisPumpStatus = "on"
		thisFanStatus = get_fan_status()
	elif deviceName == 'pump' and action == "off":
		turn_off_pump()
		thisPumpStatus = "off"
		thisFanStatus = get_fan_status()
	else:
		thisFanStatus = get_fan_status()
		thisPumpStatus = get_pump_status()
	templateData = {
		'isFanOn' : thisFanStatus,
		'isPumpOn' : thisPumpStatus,
		'humidityLevel' : thisHumidity,
		'temperature' : thisTemperature}
	return render_template('index.html', **templateData)

def get_humidity():
	with open('data.txt', 'r') as file:
		return file.readlines()[0]

def get_temperature():
	with open('data.txt', 'r') as file:
		return file.readlines()[1]
		
def get_fan_status():
	with open('data.txt', 'r') as file:
		return str(file.readlines()[2])
		
def get_pump_status():
	with open('data.txt', 'r') as file:
		return str(file.readlines()[3])
		
def get_override_status():
	with open('data.txt', 'r') as file:
		return file.readlines()[4]

def turn_on_fan():
	with open('data.txt', 'r') as file:
		data = file.readlines()
		data[2] = 'on\n'	

	with open('data.txt', 'w') as file:
		file.writelines(data)	
		print("Turning on fan")

def turn_on_pump():	
	with open('data.txt', 'r') as file:
		data = file.readlines()
		data[3] = 'on\n'	

	with open('data.txt', 'w') as file:
		file.writelines(data)
		print("Turning on pump")
	
def turn_off_fan():
	with open('data.txt', 'r') as file:
		data = file.readlines()
		data[2] = 'off\n'	

	with open('data.txt', 'w') as file:
		file.writelines(data)
		print("Turning off fan")
		
def turn_off_pump():
	with open('data.txt', 'r') as file:
		data = file.readlines()
		data[3] = 'off\n'	

	with open('data.txt', 'w') as file:
		file.writelines(data)
		print("Turning off pump")

def set_override():
	overRide = True
	with open('data.txt', 'r') as file:
		data = file.readlines()
		data[4] = '1\n'	

	with open('data.txt', 'w') as file:
		file.writelines(data)
		print("Setting Override Status")

if __name__ == '__main__':
	app.run(debug = True, port = 80, host = '0.0.0.0')
	

