import time
from gunpla.BaseGundam import BaseGundam
from phew.server import Response, Request


class NuGundam(BaseGundam):
    """
    RX-93 Nu Gundam(https://gundam.fandom.com/wiki/RX-93_ν_Gundam)
    """

    def get_config_file(self) -> str:
        """
        :return: The Nu Gundam config file
        """
        return "config/nu_gundam.json"

    def activation(self, request: Request) -> Response:
        """
        Runs the activation lightshow
        this is just a sample test
        """
        head_led = self._get_led_from_name("head")
        head_led.on()
        time.sleep(.25)
        head_led.off()
        time.sleep(.25)
        head_led.on()
        time.sleep(.25)
        head_led.off()
        return Response("finished", 200)
