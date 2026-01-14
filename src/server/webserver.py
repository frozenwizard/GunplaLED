import asyncio
import sys

from src.gunpla.generic_gundam import GenericGundam
from src.hardware.Hardware import Hardware
from src.pi.led_effect import LEDEffects
from src.server.microdot.Microdot import Microdot, Request
from src.server.microdot.utemplate import Template
from src.server.Wrappers import create_show_handler, safe_execution


class WebServer:
    """
    Webserver that manages API routes and web pages for the Gunpla
    """

    def __init__(self, configuration: dict, hardware: Hardware):
        self.app = Microdot()
        self.settings: dict = configuration
        # Instantiate the model class with hardware
        self.gundam: GenericGundam = configuration['model'](hardware)
        self.hardware: Hardware = hardware
        Template.initialize(template_dir='src/templates')

    @safe_execution
    async def index(self, request: Request):
        """
        Returns the root index page
        """
        led_list = [{"name": led.name()} for led in self.gundam.get_all_leds()]
        show_list = self.gundam.config['lightshow']

        return await Template('index.html').render_async(
            derp="Gundam LED Control",
            all_leds=led_list,
            lightshows=show_list
        ), 200, {'Content-Type': 'text/html'}

    @safe_execution
    async def canary(self, request: Request):
        """
        Sanity check to make sure webserver is running.
        """
        asyncio.create_task(LEDEffects.blink(self.hardware.board_led()))
        return "chirp", 202

    def all_on(self, request: Request):
        self.gundam.all_on()
        return "All leds are on", 202

    def all_off(self, request: Request):
        self.gundam.all_off()
        return "All leds are off", 202

    async def _connect_to_wifi(self):
        ipaddress: str = await self.hardware.networking().connect_to_wifi(self.settings['ssid'], self.settings['password'])
        if ipaddress:
            print(f"Server started on {ipaddress}")
            await LEDEffects.blink(self.hardware.board_led())
        else:
            print("Server failed to connect")
            sys.exit("Cannot start server")

    async def run(self):
        """
        Main runner of the webserver.  Loads configurations, paths, connects to wifi and runs the server
        """

        self.hardware.networking().configure_host(self.settings['hostname'])
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
        # TODO add a /stop route to stop all lightshows

        @self.app.route("/led/<led_name>/on")
        @safe_execution
        async def led_on_handler(request, led_name):
            return self.gundam.led_on(led_name)

        @self.app.route("/led/<led_name>/off")
        @safe_execution
        async def led_off_handler(request, led_name):
            return self.gundam.led_off(led_name)

        self.app.route("/all/on")(self.all_on)
        self.app.route("/all/off")(self.all_off)

        # dynamically add all lightshow paths
        for lightshow in self.gundam.config['lightshow']:
            path = f"/lightshow/{lightshow['path']}"
            method_func = getattr(self.gundam, lightshow['method'])

            self.app.route(path)(create_show_handler(method_func, self.gundam))

        # 404 Handler
        @self.app.errorhandler(404)
        def not_found(request):
            # TODO: list all routes
            return "Not found", 404
