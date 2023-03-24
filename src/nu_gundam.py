import json

from machine import Pin
from phew import server

class NuGundam:
    # head_led = Pin(1, Pin.OUT)
    fin_funnel1 = Pin(2, Pin.OUT)
    head_led = Pin("LED", Pin.OUT)

    def __init__(self):
        with open("nu_gundam.json") as fp:
            self.config: json = json.loads(fp.read())

    def add_routes(self, server: server):
        routes = []
        for individual_led in self.config['leds']:
            led_name = individual_led['name']
            server.add_route(f"/led/{led_name}/on", self.head_on, methods=["GET"])
            server.add_route(f"/led/{led_name}/off", self.head_off, methods=["GET"])
    def head_on(self, request):
        self.head_led.on()
        return "on", 200

    def head_off(self, request):
        self.head_led.off()
        return "off", 200