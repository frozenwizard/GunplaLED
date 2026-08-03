from src.hardware.Hardware import Hardware
from src.hardware.Networking import Networking
from src.pi.board_led import BoardLED


class PicoHardware(Hardware):
    """
    Abstraction to access the Raspberry Pi Pico hardware.
    """

    def __init__(self):
        from machine import PWM, Pin
        self.Pin = Pin
        self.PWM = PWM
        self._networking = Networking()
        self._board_led = BoardLED()

    def networking(self) -> Networking:
        """
        :return: networking
        """
        return self._networking

    def board_led(self) -> BoardLED:
        return self._board_led

    def get_pin(self, pin_num, mode="OUT"):
        # machine.Pin.OUT is an integer constant
        m = self.Pin.OUT if mode == "OUT" else self.Pin.IN
        return self.Pin(pin_num, m)

    def get_pwm(self, pin_obj):
        return self.PWM(pin_obj)

    def reset_pin(self, pin_obj):
        """Re-initializes the pin in place to clear PWM settings"""
        pin_obj.init(self.Pin.OUT)
        return pin_obj

    def create_led(self, pin_number: int, name: str):
        """Creates a real LED with actual GPIO pin"""
        from src.pi.LED import LED
        pin = self.get_pin(pin_number, mode="OUT")
        return LED(pin, name)
