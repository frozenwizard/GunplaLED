import asyncio
import logging
import sys

import network
from Microdot import Microdot, send_file
from Microdot import Request

from src import settings
from src.gunpla.generic_gundam import GenericGundam
from src.pi.board_led import BoardLED
from src.pi.LED import LED
from src.pi.led_effect import LEDEffects
from src.server.Wrappers import create_show_handler, safe_execution
from src.server.Networking import connect_to_wifi

class WebServer:
    """
    Webserver that manages API routes and web pages for the Gunpla
    """

    def __init__(self, configuration: dict):
        self.app = Microdot()
        self.settings: dict = configuration
        self.gundam: GenericGundam = settings.webserver['model']
        self.board_led: LED = BoardLED()

    @safe_execution
    async def index(self, request: Request):
        """
        Returns the root index page
        """
        # Todo fix this rendering
        return await send_file("src/www/index.html")

    @safe_execution
    async def canary(self, request: Request):
        """
        Sanity check to make sure webserver is running.
        """
        asyncio.create_task(LEDEffects.blink(self.board_led))
        return "chirp", 202

    async def _connect_to_wifi(self):
        ipaddress: str = connect_to_wifi(self.settings['ssid'], self.settings['password'])
        if ipaddress:
            print(f"Server started on {ipaddress}")
            await LEDEffects.blink(self.board_led)
        else:
            logging.error("Server failed to connect")
            sys.exit("Cannot start server")

    async def run(self):
        """
        Main runner of the webserver.  Loads configurations, paths, connects to wifi and runs the server
        """
        network.hostname(self.settings['hostname'])
        print(f"Set hostname to {network.hostname()}")

        await self._connect_to_wifi()

        self._add_routes()

        await self.app.start_server(host='0.0.0.0', port=80, debug=True)

    def _add_routes(self):
        """
           Given a server adds all endpoints for Leds and lightshows
        """
        self.app.route("/")(self.index)
        self.app.route("/index")(self.index)
        self.app.route("/canary")(self.canary)

        @self.app.route("/led/<led_name>/on")
        @safe_execution
        async def led_on_handler(request, led_name):
            return self.gundam.led_on(led_name)

        @self.app.route("/led/<led_name>/off")
        @safe_execution
        async def led_off_handler(request, led_name):
            return self.gundam.led_off(led_name)

        self.app.route("/all/on")(self.gundam.all_on)
        self.app.route("/all/off")(self.gundam.all_off)

        for lightshow in self.gundam.config['lightshow']:
            path = f"/lightshow/{lightshow['path']}"
            method_func = getattr(self.gundam, lightshow['method'])

            self.app.route(path)(create_show_handler(method_func))

        # 404 Handler
        @self.app.errorhandler(404)
        def not_found(request):
            return "Not found", 404
