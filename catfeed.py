from gpiozero import LED, Button
from time import sleep
import requests
from argparse import ArgumentParser

print("init")

service_root = "http://cat.chriswait.net/"
check_url = service_root
add_feed_url = service_root + "add_feed"
check_frequency_seconds = 30
button_pin = 25
led_pin = 14
debug = False

parser = ArgumentParser()
parser.add_argument('-d', action='store_true')
options = parser.parse_args()
if options.d:
    debug = True

button = Button(button_pin)
led = LED(led_pin)

def flash(num=3):
    for i in range(num):
        led.on()
        sleep(0.2)
        led.off()
        sleep(0.2)

def make_request(url):
    if debug:
        print("Making request", url)
    try:
        req = requests.get(url)
    except requests.exceptions.ConnectionError as e:
	flash()
        print("Connection", e)
        return False
    except requests.exceptions.Timeout as e:
	flash()
        print("Timeout", e)
        return False
    except requests.exceptions.RequestException as e:
	flash()
        print("Other", e)
        return False
    else:
        if (req.status_code == 200):
            if debug:
                print("Success:", req.text)
            return req.text
        else:
            return False

def add_feed():
    if debug:
        print("Adding Feed")

    if make_request(add_feed_url):
	if debug:
            print("Added feed")
        led.off()
    else:
        if debug:
            print("Failed to add feed")
button.when_pressed = add_feed

def check_should_feed():
    if debug:
        print("Checking")
    result = make_request(check_url)
    if result:
        if debug:
            print("Checked", result)
        return (result == "1")
    else:
        if debug:
            print("Failed to check feed")
    return False

flash(num=5)
if debug:
    print("Entering main loop")

while True:
    if check_should_feed():
        led.on()
    else:
        led.off()
    if debug:
        print("sleeping")
    sleep(check_frequency_seconds)

led.off()
