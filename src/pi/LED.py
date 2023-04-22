from time import sleep
from machine import Pin, PWM


class LED:
    """
    A wrapper around Pin(n, Pin.OUT) that provides LED light like functionality to turn on, turn off, dim, etc
    """

    def __init__(self, pin_number: int, name: str):
        self.pin: Pin = Pin(pin_number, Pin.OUT)
        self.led_name = name

    def on(self) -> None:
        """
        Turns on the LED light
        """
        self.pin.on()

    def off(self):
        """
        Turns off the LED light
        """
        self.pin.off()

    def name(self) -> str:
        """
        :return: The name of LED
        """
        return self.led_name

    def pin(self) -> Pin:
        """
        :return: The underlying Raspberry Pi Pico Pin of the LED.
        """
        return self.pin()

    def brighten(self, start_percent: int = 0, end_percent: int = 100, speed: int = 1) -> None:
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
