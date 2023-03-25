from abc import abstractmethod

from phew import server
import json

from machine import Pin

from phew.server import Response, Request


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
        server.add_route("/led/all/on", self.all_on, methods=["GET"])
        server.add_route(f"/led/all/off", self.all_off, methods=["GET"])
        for lightshow in self.config['lightshow']:
            server.add_route(f"/lightshow/{lightshow['path']}", getattr(self, lightshow['method']), methods=["GET"])

    def led_on(self, request: Request, led_name: str) -> Response:
        """
        Turns a Single LED on by name
        """
        try:
            pin_num = self.get_pin_from_name(led_name)
            led = self.generic_pin(pin_num)
            self.head_led.on()
            return f"{led_name} on", 200
        except Exception as e:
            return str(e), 500

    def led_off(self, request: Request, led_name: str) -> Response:
        """
        Turns a single LED off by name
        """
        try:
            pin_num = self.get_pin_from_name(led_name)
            led = self.generic_pin(pin_num)
            self.head_led.off()
            return f"{led_name} off", 200
        except Exception as e:
            return str(e), 500

    def all_on(self, request: Request)->Response:
        """
        Turns all configured LED's on.
        """
        try:
            for led in self.config['leds']:
                pin_num = led['pin']
                led = self.generic_pin(pin_num)
                led.on()
            return "All on", 200
        except Exception as e:
            return str(e), 500

    def all_off(self, request:Request) -> Response:
        """
        Turns all configured LED's off
        """
        try:
            for led in self.config['leds']:
                pin_num = led['pin']
                led = self.generic_pin(pin_num)
                led.off()
            return "All off", 200
        except Exception as e:
            return str(e), 500


    def generic_pin(self, pin_num:int) -> Pin:
        """
        Given a pin number, returns the Pin for it
        """
        return Pin(pin_num, Pin.OUT)

    def get_pin_from_name(self, led_name: str) -> int:
        """
        Given a led_name, returns the pin number associated with it
        """
        for entry in self.config['leds']:
            if entry['name'] == led_name:
                return entry['pin']
        raise Exception(f"Led '{led_name}' not found")
