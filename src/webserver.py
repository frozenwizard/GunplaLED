import sys
import network

from src import settings
from src.gunpla.GenericGundam import GenericGundam
from src.pi.LED import LED
from src.pi.board_led import BoardLED
from src.pi.led_effect import LEDEffects

from src.phew import server, connect_to_wifi
from src.phew.server import logging, Request, Response
from src.phew.template import render_template


class WebServer:
    """
    Webserver that manages API routes and web pages for the Gunpla
    """

    def __init__(self, configuration: dict):
        self.settings: dict = configuration
        self.gundam: GenericGundam = settings.webserver['model']
        self.board_led: LED = BoardLED()

    def index(self, request: Request) -> Response:
        """
        Returns the root index page
        """
        return await render_template("src/www/index.html",
                                     title=self.gundam.config['name'],
                                     all_leds=self.gundam.config['leds'],
                                     lightshows=self.gundam.config['lightshow'])

    def canary(self, request: Request) -> Response:
        """
        Sanity check to make sure webserver is running.
        """
        LEDEffects.blink(self.board_led)
        return Response("chirp", 200)

    def catchall(self, request: Request):
        """
        Generic handler to catch any routing error
        """
        return Response("Not found", 404)

    def main(self):
        """
        Main runner of the webserver.  Loads configurations, paths, connects to wifi and runs the server
        """
        network.hostname(self.settings['hostname'])
        logging.info(f"Set hostname to {network.hostname()}")
        logging.info(f"Connect to {self.settings['ssid']} with {self.settings['password']}")
        ipaddress: str = connect_to_wifi(self.settings['ssid'], self.settings['password'])
        if ipaddress:
            logging.info(f"Server started on {ipaddress}")
            LEDEffects.blink(self.board_led)
        else:
            logging.error("Server failed to connect")
            sys.exit("Cannot start server")

        server.add_route("/", self.index, methods=["GET"])
        server.add_route("/index", self.index, methods=["GET"])
        server.add_route("/canary", self.canary, methods=["GET"])
        server.set_callback(self.catchall)

        self.gundam.add_routes(server)

        server.run()
