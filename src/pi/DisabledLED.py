from pi.LED import LED


class disabled_led(LED):

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
