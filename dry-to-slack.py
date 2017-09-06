#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import httplib, urllib
import urllib2
import json

# Slack webhook
webhook_url = "ADD_HERE"

def postToSlack():
    data = '{"text": "Garden plant needs watering!"}'
    slack = urllib2.Request(webhook_url, data, {'Content-Type': 'application/json'})
    post = urllib2.urlopen(slack)
    post.close()

def moisture(channel):
    if GPIO.input(channel):
            print "LED off"
            postToSlack()
    else:
            print "LED on"
            
GPIO.setmode(GPIO.BCM)

channel = 17

GPIO.setup(channel, GPIO.IN)

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)

GPIO.add_event_callback(channel, callback)

while True:
        time.sleep(0.1)
