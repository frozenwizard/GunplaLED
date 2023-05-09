import sys
from machine import Pin
import time
import network

from src import settings
from src.phew.server import logging
from src.gunpla.GenericGundam import GenericGundam
from src.phew import server, connect_to_wifi
from src.phew.server import Request, Response
from src.phew.template import render_template


class WebServer:
    """
    Webserver that manages API routes and web pages for the Gunpla
    """

    def __init__(self, configuration: dict):
        self.settings: dict = configuration
        self.gundam: GenericGundam = settings.webserver['model']
        self.board_led: Pin = Pin("LED", Pin.OUT)

    def index(self, request: Request) -> Response:
        return await render_template("src/www/index.html",
                                     title=self.gundam.config['name'],
                                     all_buttons=self.gundam.config['leds'])

    def canary(self, request: Request) -> Response:
        """
        Sanity check to make sure webserver is running.
        """
        self.board_led.on()
        time.sleep(0.25)
        self.board_led.off()
        time.sleep(0.25)
        self.board_led.on()
        time.sleep(0.25)
        self.board_led.off()
        return Response("chirp", 200)

    def catchall(self, request: Request):
        return Response("Not found", 404)

    def blink(self) -> None:
        """
        Blinks the onboard LED twice
        """
        self.board_led.on()
        time.sleep(0.5)
        self.board_led.off()
        time.sleep(0.5)
        self.board_led.on()
        time.sleep(0.5)
        self.board_led.off()

    def main(self):
        network.hostname(self.settings['hostname'])
        logging.info(f"Set hostname to {network.hostname()}")
        logging.info(f"Connect to {self.settings['ssid']} with {self.settings['password']}")
        ipaddress: str = connect_to_wifi(self.settings['ssid'], self.settings['password'])
        if ipaddress:
            logging.info(f"Server started on {ipaddress}")
            self.blink()
        else:
            logging.error("Server failed to connect")
            sys.exit("Cannot start server")

        server.add_route("/", self.index, methods=["GET"])
        server.add_route("/index", self.index, methods=["GET"])
        server.add_route("/canary", self.canary, methods=["GET"])
        server.set_callback(self.catchall)

        self.gundam.add_routes(server)

        server.run()
