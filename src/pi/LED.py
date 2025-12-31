from machine import Pin


class LED:
    """
    A wrapper around Pin(n, Pin.OUT) that provides LED light like functionality to turn on, turn off, dim, etc
    """

    def __init__(self, pin_number: int, name: str):
        self._pin: Pin = Pin(pin_number, Pin.OUT)
        self._led_name = name

    def enabled(self) -> bool:
        """
        Returns true as the LED is connected
        """
        return True

    def on(self) -> None:
        """
        Turns on the LED light
        """
        self._pin.on()

    def off(self):
        """
        Turns off the LED light
        """
        self._pin.off()

    def name(self) -> str:
        """
        :return: The name of LED
        """
        return self._led_name

    def pin(self) -> Pin:
        """
        :return: The underlying Raspberry Pi Pico Pin of the LED.
        """
        return self._pin
