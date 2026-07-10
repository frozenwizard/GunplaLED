
from src.hardware.Networking import Networking
from src.pi.board_led import BoardLED


class Hardware:
    """
    Hardware abstraction layer.
    """

    def get_pin(self, pin_num, mode):
        raise NotImplementedError

    def get_pwm(self, pin_obj):
        raise NotImplementedError

    def reset_pin(self, pin):
        """
        Reinitializes a pin previously used for PWM back to plain digital output.
        :param pin: The Pin object to reinitialize
        :return: A Pin object ready for plain digital I/O on the same GPIO
        """
        raise NotImplementedError

    def networking(self) -> Networking:
        raise NotImplementedError

    def board_led(self) -> BoardLED:
        raise NotImplementedError

    def create_led(self, pin_number: int, name: str):
        """
        Creates an LED instance appropriate for this hardware.
        :param pin_number: GPIO pin number
        :param name: LED name
        :return: LED instance appropriate for this hardware
        """
        raise NotImplementedError
