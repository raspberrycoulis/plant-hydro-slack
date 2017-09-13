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

# Set the GPIO mode:
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin that the moisture sensor (D0 on the sensor) is connected to:
channel = 17

# Set the GPIO pin above as an input and set the internal pull-up resistor down:
GPIO.setup(channel, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

# Slack webhook - get this from https://api.slack.com/custom-integrations/incoming-webhooks
webhook_url = "ADD_HERE"

# This is the function that calls the Slack webhook to notify you:
def postToSlack():
    data = '{"attachments":[{"fallback":"Water plant!","pretext":"The soil is too dry!","color":"#cc0000","fields":[{"title":"The Garden Room plant needs watering!","short":false}]}]}'
    slack = urllib2.Request(webhook_url, data, {'Content-Type': 'application/json'})
    post = urllib2.urlopen(slack)
    post.close()

# Run the code in an infinite loop. If the soil is dry, a Slack notification is triggered:
while True:
    if GPIO.input(channel)==False:
        #print('Soil is moist')     # Uncomment to print console commands
        time.sleep(900)             # Sleep for 15 minutes (900 seconds)
    else:
        #print('Soil is dry!')      # Uncomment to print console commands
        postToSlack()               # Trigger the Slack webhook notification
        time.sleep(2700)            # Sleep for 45 minutes (2700 seconds)
