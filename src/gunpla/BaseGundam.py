import json

from src.pi.LED import LED
from src.pi.board_led import BoardLED
from src.phew.server import logging
from src.phew import server
from src.phew.server import Response, Request
from src.pi.DisabledLED import DisabledLED


class BaseGundam:
    """
    Base Gunpla.
    """
    board_led = BoardLED()

    def __init__(self):
        with open(self.get_config_file()) as config_contents:
            self.config: json = json.loads(config_contents.read())

    def get_config_file(self) -> str:
        """
        Returns the path to the corresesponding Gundam json file
        This is abstract
        """
        raise Exception("Not implemented")

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
        logging.info(f"turning on {led_name}")
        try:
            led = self._get_led_from_name(led_name)
            led.on()
            return Response(f"{led_name}: on", 200)
        except Exception as ex:
            return Response(str(ex), 500)

    def led_off(self, request: Request, led_name: str) -> Response:
        """
        Turns a single LED off by name
        """
        logging.info(f"turning off {led_name}")
        try:
            led = self._get_led_from_name(led_name)
            led.off()
            return Response(f"{led_name}: off", 200)
        except Exception as ex:
            return Response(str(ex), 500)

    def all_on(self, request: Request) -> Response:
        """
        Turns all configured LED's on.
        """
        logging.info("turning on all leds")
        try:
            leds: str = ""
            for led_entry in self.config['leds']:
                led_name = led_entry['name']
                led = self._get_led_from_name(led_name)
                led.on()
                if isinstance(led, DisabledLED):
                    leds += f"{led_name}: disabled\n"
                else:
                    leds += f"{led_name}: on\n"
            return Response(f"<html>All on\n {leds} </html>", 200)
        except Exception as ex:
            return Response(str(ex), 500)

    def all_off(self, request: Request) -> Response:
        """
        Turns all configured LED's off
        """
        logging.info("turning off all leds")
        try:
            leds: str = ""
            for led_entry in self.config['leds']:
                led_name = led_entry['name']
                led = self._get_led_from_name(led_name)
                led.off()
                if isinstance(led, DisabledLED):
                    leds += f"{led_name}: disabled\n"
                else:
                    leds += f"{led_name}: off\n"
            return Response("All off\n" + leds, 200)
        except Exception as ex:
            return Response(str(ex), 500)

    def _get_led_from_name(self, led_name: str) -> LED:
        """
        Given a name of an LED, returns the LED object for it.
        Throws an exception if it's not found
        :param led_name:
        :return:
        """
        entry = self.__get_entry_from_name(led_name)
        if 'disabled' in entry and entry['disabled']:
            logging.debug(f"{led_name} is disabled")
            return DisabledLED(led_name)
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
