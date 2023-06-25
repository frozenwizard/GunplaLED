from src.pi.LED import LED


class DisabledLED(LED):
    """
    An LED that is disabled in the configuration.  When attempted to manipulate by turning it on or off, it does nothing.
    """

    def __init__(self, led_name: str):  # pylint: disable=super-init-not-called
        self.led_name = led_name

    def enabled(self) -> bool:
        """
        Returns false as the LED is not connected
        """
        return False

    def name(self) -> str:
        return self.led_name

    def pin(self):
        return None

    def on(self):
        pass

    def off(self):
        pass
