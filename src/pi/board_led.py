from src.pi.LED import LED


class BoardLED(LED):
    """
    Special Representation of the onboard Pico LED
    """

    def __init__(self):  # pylint  # pylint: disable=(super-init-not-called
        from machine import Pin

        self._pin: Pin = Pin("LED", Pin.OUT)
        self._led_name = "Board LED"
