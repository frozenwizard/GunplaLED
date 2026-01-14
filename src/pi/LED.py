

class LED:
    """
    A wrapper around Pin(n, Pin.OUT) that provides LED light like functionality to turn on, turn off, dim, etc
    """

    def __init__(self, pin, name: str):
        """
        :param pin: A Pin object (from machine.Pin or MockPin)
        :param name: The LED name
        """
        self._pin = pin
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

    def pin(self):
        """
        :return: The underlying Raspberry Pi Pico Pin of the LED.
        """
        return self._pin


class MockLED(LED):
    """
    LED implementation for simulation that prints actions to console.
    Used when running with VirtualHardware for testing without physical hardware.
    """

    def on(self):
        """Turns on the LED with simulation output"""
        print(f"[SIM] LED '{self._led_name}' (Pin {self._pin.num}) ON")
        self._pin.on()

    def off(self):
        """Turns off the LED with simulation output"""
        print(f"[SIM] LED '{self._led_name}' (Pin {self._pin.num}) OFF")
        self._pin.off()
