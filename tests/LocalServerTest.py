
import asyncio
import json

from src.gunpla.generic_gundam import GenericGundam
from src.hardware.VirtualHardware import VirtualHardware
from src.server.webserver import WebServer

"""
Sanity check class to run the webserver in local mode when a Raspberry pi is not needed.
"""


class MobileDoll(GenericGundam):
    """
    Mobile Doll
    """

    def __init__(self, hardware, model_config: json = None):
        self.hardware = hardware
        self.config = model_config if model_config else {}

    def get_config_file(self) -> str:
        return "tests/config/virgo.json"

    async def activation(self):
        print("Mobile Doll activation")
        return

    async def infinite(self):
        try:
            while True:
                await asyncio.sleep(1)
                print("Hi")
        except asyncio.CancelledError:
            print("Infinite loop cancelled")
            raise


def main():

    model_config = {
        "$schema": "gundam_led_config.schema.json",

        "name": "Virgo",
        "leds": [
            {"name":  "head", "pin": 0, "color":  "green", "disabled":  False},
        ],
        "lightshow": [
            {
                "name": "Activate Virgo",
                "path": "activation",
                "method": "activation"
            },
            {
                "name": "Infinitelooop test",
                "path": "infinite",
                "method": "infinite"
            }
        ]
    }

    test_settings = {
        "ssid": "wifi",
        "password": 'wifi-pass',
        "hostname": 'virgo',
        "model": lambda hardware: MobileDoll(hardware, model_config)
    }

    webserver = WebServer(test_settings, VirtualHardware())
    asyncio.run(webserver.run())


if __name__ == "__main__":
    main()
