# This is a test file meant to be deployed as an initial test to make sure the env is setup correctly.
# This requires just the basic Raspberry Pi Pico W
# Once deployed on the Pico W, it will flash the onboard LED.

import time

from machine import Pin


def main():
    """
    Blinks the onboard Raspberry Pi Pico W LED several times.
    """
    led = Pin("LED", Pin.OUT)
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)


if __name__ == "__main__":
    main()
