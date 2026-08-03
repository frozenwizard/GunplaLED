import asyncio
import sys

from src.gunpla.generic_gundam import GenericGundam
from src.hardware.Hardware import Hardware
from src.pi.led_effect import LEDEffects
from src.server.lightshow_manager import LightshowManager
from src.server.microdot.Microdot import Microdot, Request
from src.server.microdot.utemplate import Template
from src.server.Wrappers import create_show_handler, safe_execution


def run_server(settings: dict, hardware: Hardware) -> None:
    """
    Composes and runs the webserver.  The single entry point shared by the
    on-device runner (main.py) and the local test server (tests/LocalServerTest.py).
    """
    webserver = WebServer(settings, hardware)
    asyncio.run(webserver.run())


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
        self.show_manager = LightshowManager(self.gundam)
        Template.initialize(template_dir='src/templates')

    @safe_execution
    async def index(self, request: Request):
        """
        Returns the root index page
        """
        led_list = [{"name": led.name()} for led in self.gundam.get_all_leds()]
        show_list = self.gundam.config['lightshow']
        return await Template('index.html').render_async(
            name_of_title="Gundam LED Control",
            all_leds=led_list,
            lightshows=show_list,
            status_message=self.show_manager.describe()
        ), 200, {'Content-Type': 'text/html'}

    @safe_execution
    async def canary(self, request: Request):
        """
        Sanity check to make sure webserver is running.
        """
        asyncio.create_task(LEDEffects.blink(self.hardware.board_led()))
        return "chirp", 202

    async def all_on(self, request: Request):
        """
          Turns on all LEDs, halting any running lightshow first.
          :param request:  Ignored.
          :return: HTTP 202 and message
          """
        await self.show_manager.run_action("All LEDs on", self.gundam.all_on)
        return "All leds are on", 202

    async def all_off(self, request: Request):
        """
        Turns off all LEDs, halting any running lightshow first.
        :param request:  Ignored.
        :return: HTTP 202 and message
        """
        await self.show_manager.run_action("All LEDs off", self.gundam.all_off)
        return "All leds are off", 202

    async def _connect_to_wifi(self):
        """
        Attempts to connect the Pico to WiFi.  If succesful, will blink the onboard LED.
        If it fails, it will halt the system.
        """
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

        await self.app.start_server(
            host=self.settings.get('host', '0.0.0.0'),
            port=self.settings.get('port', 80),
            debug=self.settings.get('debug', True))

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
            # Validate before run_action, which cancels any running show — an
            # unknown led_name shouldn't destroy a show just to then 500.
            if not self.gundam.has_led(led_name):
                raise Exception(f"Entry '{led_name}' not found")
            await self.show_manager.run_action(f"LED '{led_name}' on", lambda: self.gundam.led_on(led_name))

        @self.app.route("/led/<led_name>/off")
        @safe_execution
        async def led_off_handler(request, led_name):
            if not self.gundam.has_led(led_name):
                raise Exception(f"Entry '{led_name}' not found")
            await self.show_manager.run_action(f"LED '{led_name}' off", lambda: self.gundam.led_off(led_name))

        self.app.route("/all/on")(self.all_on)
        self.app.route("/all/off")(self.all_off)

        # dynamically add all lightshow paths
        for lightshow in self.gundam.config['lightshow']:
            path = f"/lightshow/{lightshow['path']}"
            method_func = getattr(self.gundam, lightshow['method'])

            self.app.route(path)(create_show_handler(lightshow['name'], method_func, self.show_manager))

        @self.app.route("/lightshow/stop")
        @safe_execution
        async def stop_lightshow(request):
            """
            Stops any currently running lightshow task on the gundam instance.
            Stop always leaves all the LEDs off, running show or not.
            """
            stopped_show = await self.show_manager.stop()
            if stopped_show:
                return {"status": "stopped", "message": f"Lightshow '{stopped_show}' terminated"}, 200
            return {"status": "idle", "message": "No active lightshow to stop"}, 200

        @self.app.route("/lightshow/status")
        @safe_execution
        async def lightshow_status(request):
            """
            Reports the current lightshow status as JSON.
            """
            status = self.show_manager.status()
            status["message"] = self.show_manager.describe()
            return status, 200

        # 404 Handler
        @self.app.errorhandler(404)
        async def not_found(request):
            # Microdot stores routes in the url_map which is a tuple
            urls: list[str] = []
            for route in self.app.url_map:
                # route is a tuple: (method, path_re, handler)
                path = route[1].url_pattern  # The regex pattern of the URL

                if "<led_name>" in path:
                    x = [led.name() for led in self.gundam.get_all_leds() if led.enabled()]
                    for led_name in x:
                        complete_path = path.replace("<led_name>", led_name)
                        urls.append(complete_path)
                else:
                    urls.append(path)

            return await Template('404.html').render_async(
                name_of_title="404",
                urls=urls,
            ), 404, {'Content-Type': 'text/html'}
