
import uasyncio
import json

from src.gunpla.generic_gundam import GenericGundam
from src.hardware.VirtualHardware import VirtualHardware
from src.server.webserver import WebServer


class DummyPlug(GenericGundam):

    def __init__(self, model_config: json):
        self.config = model_config

    def get_config_file(self) -> str:
        return "tests/config/dummy_plug.json"

    # TODO: refactor light show url creation to be a decorator and also not need the request.
    async def activation(self):
        print("Dummy Plug activation")
        return


def main():

    model_config = {
        "$schema": "gundam_led_config.schema.json",

        "name": "dummy plug",
        "leds": [
            {"name":  "head", "pin": 0, "color":  "green", "disabled":  True},
        ],
        "lightshow": [
            {
                "name": "Activate Gundam",
                "path": "activation",
                "method": "activation"
            }
        ]
    }

    test_settings = {
        "ssid": "wifi",
        "password": 'wifi-pass',
        "hostname": 'rei',
        "model": DummyPlug(model_config)
    }

    webserver = WebServer(test_settings, VirtualHardware())
    uasyncio.run(webserver.run())


if __name__ == "__main__":
    main()
