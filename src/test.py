#This is a test file meant to be deployed as an initial test to make sure the env is setup correctly.
#This requires just the basic Raspberry Pi Pico W
#Once deployed on the Pico W, it will flash the onboard LED.

from machine import Pin, Timer

led = Pin("LED", Pin.OUT)
tim = Timer()
def tick(timer):
    global led
    led.toggle()

tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)