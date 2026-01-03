import sys

from src.hardware.Hardware import Hardware
from src.hardware.PicoHardwre import PicoHardware
from src.hardware.VirtualHardware import VirtualHardware


def get_hardware() -> Hardware:
    """
    :return: the appropriate hardware
    """
    if sys.platform == 'rp2':
        return PicoHardware()
    return VirtualHardware()
