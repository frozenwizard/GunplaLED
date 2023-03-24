from abc import abstractmethod

from phew import server
import json

from machine import Pin


class BaseGundam:
    head_led = Pin("LED", Pin.OUT)

    def __init__(self):
        with open(self.get_config_file()) as fp:
            self.config: json = json.loads(fp.read())

    @abstractmethod
    def get_config_file(self)->str:
        pass

    def add_routes(self, server: server):
        server.add_route(f"/led/<led_name>/on", self.led_on, methods=["GET"])
        server.add_route(f"/led/<led_name>/off", self.led_off, methods=["GET"])
        for lightshow in self.config['lightshow']:
            server.add_route(f"/lightshow/{lightshow['path']}", getattr(self, lightshow['method']), methods=["GET"])

    def led_on(self, request, led_name):
        try:
            pin_num = self.get_pin_from_name(led_name)
            led = self.generic_pin(pin_num)
            self.head_led.on()
            return f"{led_name} on", 200
        except Exception as e:
            return str(e), 500

    def led_off(self, request, led_name):
        try:
            pin_num = self.get_pin_from_name(led_name)
            led = self.generic_pin(pin_num)
            self.head_led.off()
            return f"{led_name} off", 200
        except Exception as e:
            return str(e), 500

    def generic_pin(self, pin_num) -> Pin:
        return Pin(pin_num, Pin.OUT)

    def get_pin_from_name(self, led_name: str) -> int:
        for entry in self.config['leds']:
            if entry['name'] == led_name:
                return entry['pin']
        raise Exception(f"Led '{led_name}' not found")
