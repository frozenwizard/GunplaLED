from machine import Pin, PWM
from time import sleep


class LED:

    def __init__(self, pin_number: int, name: str):
        self.pin: Pin = Pin(pin_number, Pin.OUT)
        self.name = name

    def on(self):
        self.pin.on()

    def off(self):
        self.pin.off()

    def name(self) -> str:
        return self.name()

    def pin(self) -> Pin:
        return self.pin()

    def brighten(self, start_percent:int =0, end_percent:int =100, speed: int = 1)-> None:
        """
        Starting from start_pct goes to end_pct over the course of speed
        :param intensity:
        :param speed:
        :return:
        """
        pwm = PWM(self.pin())
        pwm.freq(1000)
        start = int((65025 * start_percent) / 100)
        end = int((65025 * end_percent) / 100)

        for duty in range(start, end):
            pwm.duty_u16(duty)
            sleep(0.0001)