
from pi.LED import LED
from phew import server
import json

from machine import Pin

from phew.server import Response, Request
from pi.DisabledLED import DisabledLED


class BaseGundam:
    board_led = Pin("LED", Pin.OUT)

    def __init__(self):
        with open(self.get_config_file()) as config_contents:
            self.config: json = json.loads(config_contents.read())

    def get_config_file(self) -> str:
        """
        Returns the path to the corresesponding Gundam json file
        This is abstract
        """
        pass

    def add_routes(self, webserver: server) -> None:
        """
        Given a server adds all endpoints for Leds and lightshows
        """
        webserver.add_route("/led/<led_name>/on", self.led_on, methods=["GET"])
        webserver.add_route("/led/<led_name>/off", self.led_off, methods=["GET"])
        webserver.add_route("/all/on", self.all_on, methods=["GET"])
        webserver.add_route("/all/off", self.all_off, methods=["GET"])
        for lightshow in self.config['lightshow']:
            webserver.add_route(f"/lightshow/{lightshow['path']}", getattr(self, lightshow['method']), methods=["GET"])

    def led_on(self, request: Request, led_name: str) -> Response:
        """
        Turns a Single LED on by name
        """
        try:
            print(f"turning on {led_name}")
            led = self._get_led_from_name(led_name)
            led.on()
            return f"{led_name} on", 200
        except Exception as ex:
            return str(ex), 500

    def led_off(self, request: Request, led_name: str) -> Response:
        """
        Turns a single LED off by name
        """
        try:
            led = self._get_led_from_name(led_name)
            led.off()
            return f"{led_name} off", 200
        except Exception as ex:
            return str(ex), 500

    def all_on(self, request: Request) -> Response:
        """
        Turns all configured LED's on.
        """
        try:
            for led_entry in self.config['leds']:
                led_name = led_entry['pin']
                led = self._get_led_from_name(led_name)
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
                led = self._get_led_from_name(led_name)
                led.off()
            return "All off", 200
        except Exception as e:
            return str(e), 500

    def _get_led_from_name(self, led_name: str) -> LED:
        """
        Given a name of an LED, returns the LED object for it.
        Throws an exception if it's not found
        :param led_name:
        :return:
        """
        entry = self.__get_entry_from_name(led_name)
        print(entry)
        if 'disabled' in entry and entry['disabled']:
            return DisabledLED()
        return LED(entry['pin'], led_name)

    def __get_entry_from_name(self, led_name: str) -> json:
        """
        Given an LED name, returns the corresponding JSON config entry for it.
        :param led_name:
        :return:
        """
        for entry in self.config['leds']:
            if entry['name'] == led_name:
                return entry
        raise Exception(f"Entry '{led_name}' not found")