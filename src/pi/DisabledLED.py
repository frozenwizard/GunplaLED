from src.pi.LED import LED


class DisabledLED(LED):
    """
    An LED that is disabled in the configuration.  When attempted to manipulate by turning it on or off, it does nothing.
    """

    def __init__(self, led_name: str):
        self.led_name = led_name

    def name(self) -> str:
        return self.led_name

    def pin(self):
        return None

    def on(self):
        pass

    def off(self):
        pass

    def brighten(self, start_percent: int = 0, end_percent: int = 100, speed: int = 1) -> None:
        pass
