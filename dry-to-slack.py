#!/usr/bin/python

#####################################################################################
# This was inspired by a guide on ModMyPi (http://bit.ly/mmpsms).                   #
#                                                                                   #
# Use a soil moisture sensor and a Raspberry Pi to monitor the soil in a plant pot  #
# and warn the office, via Slack, that it needs watering.                           #
#                                                                                   #
# By Wesley Archer (@raspberrycoulis - https://www.raspberrycoulis.co.uk)           #
#####################################################################################

# Import the necessary libraries:
import RPi.GPIO as GPIO
import time
import httplib, urllib
import urllib2
import json

# Slack webhook - get this from https://api.slack.com/custom-integrations
webhook_url = "ADD_HERE"

# This is the function that calls the Slack webhook to notify you:
def postToSlack():
    data = '{"attachments":[{"fallback":"Water plant!","pretext":"The soil is too dry!","color":"#cc0000","fields":[{"title":"The Garden Room plant needs watering!","short":false}]}]}'
    slack = urllib2.Request(webhook_url, data, {'Content-Type': 'application/json'})
    post = urllib2.urlopen(slack)
    post.close()

# This is the function that checks if the soil is moist or dry:
def moisture(channel):
    if GPIO.input(channel):
            #print "Soil is dry!"    # Uncomment to show feedback in console
            postToSlack()
    else:
            #print "Soil is moist"   # Uncomment to show feedback in console
            return "Soil is moist"

# Set the GPIO mode:
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin that the moisture sensor (D0 on the sensor) is connected to:
channel = 17

# Set the GPIO pin above as an input:
GPIO.setup(channel, GPIO.IN)

# Check whether the GPIO pin is high or low. The bouncetime is the minimum time between two callbacks (default=300) in millseconds:
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)

# This line assigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function:
GPIO.add_event_callback(channel, moisture)

# Run the code in an infinite loop and tells the script to wait 0.1 seconds, this is so the script doesnt hog all of the CPU:
while True:
        time.sleep(0.1)
