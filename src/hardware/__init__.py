import sys

from src.hardware.Hardware import Hardware


def get_hardware() -> Hardware:
    """
    :return: the appropriate hardware

    Imports are done lazily so the Pico never loads the mock implementation
    (and the laptop never touches machine/network).
    """
    if sys.platform == 'rp2':
        from src.hardware.PicoHardwre import PicoHardware
        return PicoHardware()
    from src.hardware.VirtualHardware import VirtualHardware
    return VirtualHardware()
