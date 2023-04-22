from LED import LED


class DisabledLED(LED):
    def on(self):
        pass

    def off(self):
        pass

    def brighten(self, start_percent: int = 0, end_percent: int = 100, speed: int = 1) -> None:
        pass
