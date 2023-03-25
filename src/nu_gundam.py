import json

from machine import Pin
import time
from BaseGundam import BaseGundam
from phew import server
from phew.server import Response, Request


class NuGundam(BaseGundam):
    # head_led = Pin(1, Pin.OUT)
    fin_funnel1 = Pin(2, Pin.OUT)

    def __init__(self):
        super().__init__()

    def get_config_file(self) -> str:
        return "config/nu_gundam.json"

    def activation(self, request: Request) -> Response:
        """
        Runs the activation lightshow
        """
        self.head_led.on()
        time.sleep(.25)
        self.head_led.off()
        time.sleep(.25)
        self.head_led.on()
        time.sleep(.25)
        self.head_led.off()
        return "finished", 200
