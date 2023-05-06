from machine import Pin
import time
import network

import settings

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

    @server.route("/index", methods=["GET"])
    def index(self, request: Request) -> Response:
        return await render_template("www/index.html", all_buttons=self.gundam.config['leds'])

    @server.route("/", methods=["GET"])
    def root(self, request: Request) -> Response:
        return self.index(request)

    @server.route("/canary", methods=["GET"])
    def sanity(self, request: Request) -> Response:
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

    @server.catchall()
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
        network.hostname(self.configuration['hostname'])
        src.phew.server.logging.info(f"Set hostname to {network.hostname()}")
        src.phew.server.logging.info(f"Connect to {self.configuration['ssid']} with {self.configuration['password']}")
        ipaddress: str = connect_to_wifi(self.configuration['ssid'], self.configuration['password'])
        if ipaddress:
            src.phew.server.logging.info(f"Server started on {ipaddress}")
            self.blink()
        else:
            src.phew.server.logging.error("Server failed to connect")
        self.gundam.add_routes(server)
        server.run()
