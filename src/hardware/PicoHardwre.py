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
        self.networking = Networking()
        self.board_led = BoardLED()

    def networking(self):
        """
        :return: networking
        """
        return self.networking

    def board_led(self):
        return self.board_led

    def get_pin(self, pin_num, mode="OUT"):
        # machine.Pin.OUT is an integer constant
        m = self.Pin.OUT if mode == "OUT" else self.Pin.IN
        return self.Pin(pin_num, m)

    def get_pwm(self, pin_obj):
        return self.PWM(pin_obj)

    def reset_pin(self, pin_num):
        """Re-initializes the pin to clear PWM settings"""
        return self.get_pin(pin_num, mode="OUT")
