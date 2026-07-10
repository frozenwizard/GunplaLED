from src.pi.LED import LED


class BoardLED(LED):
    """
    Special Representation of the onboard Pico LED
    """

    def __init__(self, pin=None):
        """
        :param pin: The pin driving the onboard LED.  Defaults to the real Pico pin;
                    virtual hardware injects a mock instead.
        """
        if pin is None:
            from machine import Pin
            pin = Pin("LED", Pin.OUT)
        super().__init__(pin, "Board LED")
