import src.hardware
from src.hardware.Hardware import Hardware
from src.hardware.Networking import Networking
from src.pi.board_led import BoardLED


class VirtualHardware(Hardware):
    """
    Virtual Hardware
    Fake implementation so the webserver can run without a physical Raspberry Pi Pico connected to it.
    """
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

    class MockBoardLED(BoardLED):
        """
        Fake implementation of the onboard led.
        """

        def __init__(self):
            self._pin = src.hardware.VirtualHardware.MockPin(1)
            self.led_name = "Mock Board LED"

    def __init__(self):
        self.pin = self.MockPin
        self.pwm = self.MockPWM

    def get_pin(self, pin_num, mode="OUT"):
        return self.pin(pin_num)

    def get_pwm(self, pin_obj):
        return self.pwm(pin_obj)

    def board_led(self) -> BoardLED:
        return self.MockBoardLED()

    def networking(self) -> Networking:
        return self.NoOpNetworking()

    def reset_pin(self, pin_num):
        print(f"[SIM] Pin {pin_num} reset to standard GPIO")
