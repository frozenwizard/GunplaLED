
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

    def reset_pin(self, pin_num):
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
        :return: LED instance (LED or MockLED)
        """
        raise NotImplementedError
