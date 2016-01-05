#!/bin/python
# -*- coding: utf-8 -*-
# show the battery state

import glob

def showBatteryStatus():
	Battery = 0
	for BatteryPath in glob.glob("/sys/class/power_supply/BAT?"):
		Battery += 1
		try:
			BatteryStatus = open(BatteryPath + "/status", "r")
			Status = BatteryStatus.read()
			BatteryStatus.close()
			Message = Status
			if Status.find("Full") == 0:
				# Battery is Full
				Message = "Battery " + str(Battery) + " is full" #Battery is full
			else:
				BatteryFull = open(BatteryPath + "/charge_full", "r")
				Full = int( BatteryFull.read())
				BatteryFull.close()
			
				BatteryCurrent = open(BatteryPath + "/charge_now", "r")
				Current = int( BatteryCurrent.read())
	
				if Status.find("Charging") == 0:
					# Label for Battery Charging
					Status = "Battery " +str(Battery)+" " +  " charging" # Charging
				if Status.find("Discharging") == 0:
					# Label for Battery Discharging
					Status =  "Battery " +str(Battery)+" " +  " discharging" # Discharging
		
				Percent = int( Current / Full * 100)
				# Charging/Discharging XX Percent
				Message = Status + " "+ str( Percent) + " Percent" #Percent

		except IOError:
			Message = "Battery " +str(Battery) +  " could not opened." # Battery can not open	

		print(Message)
		
	if (Battery == 0):
		Message = "No Battery found."
		print(Message)

showBatteryStatus()
