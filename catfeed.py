from gpiozero import LED, Button
from datetime import datetime, timedelta
from signal import pause
from time import sleep
from requests import post
from json import dumps

service_root = "http://cat.chriswait.net/"

button = Button(25)
led = LED(14)
led.off()

def add_feed():
    url = service_root + "add_feed"
    req = post(url)
    print req.text
button.when_pressed = add_feed

def check_should_feed():
    url = service_root
    req = post(url)
    return req.text

while True:
    sleep(10)
    print check_should_feed()
