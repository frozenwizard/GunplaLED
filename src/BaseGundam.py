
from LED import LED
from phew import server
import json

from machine import Pin

from phew.server import Response, Request
from src.DisabledLED import DisabledLED


class BaseGundam:
    head_led = Pin("LED", Pin.OUT)

    def __init__(self):
        with open(self.get_config_file()) as fp:
            self.config: json = json.loads(fp.read())

    def get_config_file(self) -> str:
        pass

    def add_routes(self, server: server):
        server.add_route(f"/led/<led_name>/on", self.led_on, methods=["GET"])
        server.add_route(f"/led/<led_name>/off", self.led_off, methods=["GET"])
        server.add_route("/all/on", self.all_on, methods=["GET"])
        server.add_route("/all/off", self.all_off, methods=["GET"])
        for lightshow in self.config['lightshow']:
            server.add_route(f"/lightshow/{lightshow['path']}", getattr(self, lightshow['method']), methods=["GET"])

    def led_on(self, request: Request, led_name: str) -> Response:
        """
        Turns a Single LED on by name
        """
        try:
            led = self.get_led_from_name(led_name)
            led.on()
            return f"{led_name} on", 200
        except Exception as e:
            return str(e), 500

    def led_off(self, request: Request, led_name: str) -> Response:
        """
        Turns a single LED off by name
        """
        try:
            led = self.get_led_from_name(led_name)
            led.off()
            return f"{led_name} off", 200
        except Exception as e:
            return str(e), 500

    def all_on(self, request: Request) -> Response:
        """
        Turns all configured LED's on.
        """
        try:
            for led_entry in self.config['leds']:
                led_name = led_entry['pin']
                led = self.get_led_from_name(led_name)
                led.on()
            return "All on", 200
        except Exception as e:
            return str(e), 500

    def all_off(self, request: Request) -> Response:
        """
        Turns all configured LED's off
        """
        try:
            for led_entry in self.config['leds']:
                led_name = led_entry['pin']
                led = self.get_led_from_name(led_name)
                led.off()
            return "All off", 200
        except Exception as e:
            return str(e), 500

    def get_led_from_name(self, led_name: str) -> LED:
        entry = self.get_entry_from_name(led_name)
        if entry['disabled']:
            return DisabledLED()
        else:
            return LED(entry['pin'], led_name)

    def get_entry_from_name(self, led_name: str) -> json:
        for entry in self.config['leds']:
            if entry['name'] == led_name:
                return entry
        raise Exception(f"Entry '{led_name}' not found")
