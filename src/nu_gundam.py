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
        server.add_route(f"/led/<led_name>/on", self.head_on, methods=["GET"])
        server.add_route(f"/led/<led_name>/off", self.head_off, methods=["GET"])


    def generic_pin(self, pin_num)->Pin:
        return Pin(pin_num, Pin.OUT)

    def get_pin_from_name(self, led_name: str)->int:
        for entry in self.config['leds']:
            if(entry['name']==led_name):
                return entry['pin']
        raise Exception(f"Led '{led_name}' not found")

    def head_on(self, request, led_name):
        try:
            pin_num = self.get_pin_from_name(led_name)
            pin = self.generic_pin(pin_num)
            self.head_led.on()
            return f"{led_name} on", 200
        except Exception as e:
            return e.__str__(), 400

    def head_off(self, request, led_name):
        try:
            pin_num = self.get_pin_from_name(led_name)
            pin = self.generic_pin(pin_num)
            self.head_led.off()
            return f"{led_name} off", 200
        except Exception as e:
            return e.__str__(), 400
