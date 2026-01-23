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
        running_show = self._is_lightshow_running()
        return await Template('index.html').render_async(
            name_of_title="Gundam LED Control",
            all_leds=led_list,
            lightshows=show_list,
            running_show=running_show
        ), 200, {'Content-Type': 'text/html'}

    @safe_execution
    async def canary(self, request: Request):
        """
        Sanity check to make sure webserver is running.
        """
        asyncio.create_task(LEDEffects.blink(self.hardware.board_led()))
        return "chirp", 202

    def all_on(self, request: Request):
        """
          Turns on all LEDs.
          :param request:  Ignored.
          :return: HTTP 202 and message
          """
        self.gundam.all_on()
        return "All leds are on", 202

    def all_off(self, request: Request):
        """
        Turns off all LEDs.
        :param request:  Ignored.
        :return: HTTP 202 and message
        """
        self.gundam.all_off()
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

        await self.app.start_server(host='0.0.0.0', port=80, debug=True)

    def _is_lightshow_running(self):
        """
        :return: True if lightshow is running, False otherwise
        """
        existing_task = getattr(self.gundam, "current_task", None)
        return existing_task is not None

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

        self.app.route("/all/on")(self.all_on)
        self.app.route("/all/off")(self.all_off)

        # dynamically add all lightshow paths
        for lightshow in self.gundam.config['lightshow']:
            path = f"/lightshow/{lightshow['path']}"
            method_func = getattr(self.gundam, lightshow['method'])

            self.app.route(path)(create_show_handler(method_func, self.gundam))

        @self.app.route("/lightshow/stop")
        @safe_execution
        async def stop_lightshow(request):
            """
            Stops any currently running lightshow task on the gundam instance.
            """
            existing_task = getattr(self.gundam, "current_task", None)

            if existing_task and not existing_task.done():
                existing_task.cancel()
                try:
                    # Wait for the task to acknowledge the cancellation
                    await existing_task
                except asyncio.CancelledError:
                    pass

                self.gundam.all_off()
                return {"status": "stopped", "message": "Lightshow terminated"}, 200

            self.gundam.all_off()
            return {"status": "idle", "message": "No active lightshow to stop"}, 200

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
