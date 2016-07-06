from gpiozero import LED, Button
from datetime import datetime, timedelta
from signal import pause
from time import sleep
from requests import get
from json import dumps

service_root = "http://cat.chriswait.net/"

button = Button(25)
led = LED(14)
led.off()

def add_feed():
    url = service_root + "add_feed"
    req = get(url)
button.when_pressed = add_feed

def check_should_feed():
    url = service_root
    req = get(url)
    return (req.text=="1")

while True:
    sleep(10)
    if check_should_feed():
        led.on()
    else:
        led.off()
