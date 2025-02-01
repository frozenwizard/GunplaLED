from machine import Pin

from src.pi.LED import LED


class BoardLED(LED):
    """
    Special Representation of the onboard Pico LED
    """

    def __init__(self):  # pylint  # pylint: disable=(super-init-not-called
        self.pin: Pin = Pin("LED", Pin.OUT)
        self.led_name = "Board LED"
