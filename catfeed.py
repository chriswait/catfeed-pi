from gpiozero import LED, Button
from datetime import datetime, timedelta
from signal import pause
from time import sleep
from requests import get
from json import dumps

service_root = "http://cat.chriswait.net/"
check_url = service_root
add_feed_url = service_root + "add_feed"
check_frequency_seconds = 60
button_pin = 25
led_pin = 14

button = Button(button_pin)
led = LED(led_pin)

def add_feed():
    req = get(add_feed_url)
button.when_pressed = add_feed

def check_should_feed():
    req = get(check_url)
    if (req.status_code == 200):
        return (req.text == "1")
    return False

while True:
    sleep(check_frequency_seconds)
    if check_should_feed():
        led.on()
    else:
        led.off()
