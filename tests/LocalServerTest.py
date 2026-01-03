
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

    def __init__(self, model_config: json):
        self.config = model_config

    def get_config_file(self) -> str:
        return "tests/config/virgo.json"

    # TODO: refactor light show url creation to be a decorator and also not need the request.
    async def activation(self):
        print("Mobile Doll activation")
        return


def main():

    model_config = {
        "$schema": "gundam_led_config.schema.json",

        "name": "Virgo",
        "leds": [
            {"name":  "head", "pin": 0, "color":  "green", "disabled":  True},
        ],
        "lightshow": [
            {
                "name": "Activate Virgo",
                "path": "activation",
                "method": "activation"
            }
        ]
    }

    test_settings = {
        "ssid": "wifi",
        "password": 'wifi-pass',
        "hostname": 'virgo',
        "model": MobileDoll(model_config)
    }

    webserver = WebServer(test_settings, VirtualHardware())
    asyncio.run(webserver.run())


if __name__ == "__main__":
    main()
