from machine import Pin


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
        return self.pin
