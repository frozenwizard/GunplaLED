from src.hardware.Hardware import Hardware
from src.hardware.Networking import Networking
from src.pi.board_led import BoardLED
from src.pi.LED import LED


class MockPin:
    """
    Partial implementation of Pico Pin, only using the currently needed methods
    """

    def __init__(self, num):
        self.num = num

    def on(self):
        print(f"[SIM] Pin {self.num} ON")

    def off(self):
        print(f"[SIM] Pin {self.num} OFF")


class MockPWM:
    """
    Partial implementation of Pico PWM, only using the currently needed methods
    """

    def __init__(self, p):
        self.p = p

    def freq(self, f):
        pass

    def duty_u16(self, d):
        print(f"[SIM] PWM {self.p.num} @ {d}")

    def deinit(self):
        print(f"[SIM] PWM {self.p.num} De-initialized")


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


class NoOpNetworking(Networking):
    """
    Networking implementation that does nothing
    """

    def __init__(self):
        pass

    async def connect_to_wifi(self, ssid: str, password: str, attempts=10) -> str:
        return "123.123.123.123"

    def configure_host(self, host_name: str):
        pass


class VirtualHardware(Hardware):
    """
    Virtual Hardware
    Fake implementation so the webserver can run without a physical Raspberry Pi Pico connected to it.
    """

    def __init__(self):
        # Cached like PicoHardware, so both implementations behave the same
        self._networking = NoOpNetworking()
        self._board_led = BoardLED(MockPin("LED"))

    def get_pin(self, pin_num, mode="OUT"):
        return MockPin(pin_num)

    def get_pwm(self, pin_obj):
        return MockPWM(pin_obj)

    def board_led(self) -> BoardLED:
        return self._board_led

    def networking(self) -> Networking:
        return self._networking

    def reset_pin(self, pin_obj):
        print(f"[SIM] Pin {pin_obj.num} reset to standard GPIO")
        return pin_obj

    def create_led(self, pin_number: int, name: str):
        """Creates a mock LED for simulation"""
        return MockLED(self.get_pin(pin_number), name)
