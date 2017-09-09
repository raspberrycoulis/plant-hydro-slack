#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import httplib, urllib
import urllib2
import json

# Slack webhook
webhook_url = "ADD_HERE"

def postToSlack():
    data = '{"attachments":[{"fallback":"Water plant!","pretext":"The soil is too dry!","color":"#cc0000","fields":[{"title":"The Garden Room plant needs watering!","short":false}]}]}'
    slack = urllib2.Request(webhook_url, data, {'Content-Type': 'application/json'})
    post = urllib2.urlopen(slack)
    post.close()

def moisture(channel):
    if GPIO.input(channel):
            #print "Soil is dry!"    # Uncomment to show feedback in console
            postToSlack()
    else:
            #print "Soil is moist"   # Uncomment to show feedback in console
            return "Soil is moist"

GPIO.setmode(GPIO.BCM)

channel = 17

GPIO.setup(channel, GPIO.IN)

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)

GPIO.add_event_callback(channel, moisture)

while True:
        time.sleep(0.1)
