import time
from src.gunpla.BaseGundam import BaseGundam
from src.phew.server import Response, Request
from src.pi import LED
from src.pi.led_effect import LEDEffects


class NuGundam(BaseGundam):
    """
    RX-93 Nu Gundam(https://gundam.fandom.com/wiki/RX-93_ν_Gundam)
    """

    def get_config_file(self) -> str:
        """
        :return: The Nu Gundam config file
        """
        return "src/config/nu_gundam.json"

    def activation(self, request: Request) -> Response:
        """
        Runs the activation lightshow
        this is just a sample test
        """
        head_led = self._get_led_from_name("head")
        head_led.on()
        time.sleep(0.1)
        head_led.off()
        time.sleep(0.5)
        LEDEffects.brighten(head_led)
        return Response("finished", 200)

    def fire_funnels(self, request: Request) -> Response:
        """
        Light Show that fires fin funnels in order
        """
        fin1: LED = self._get_led_from_name("fin_funnel_1")
        fin2: LED = self._get_led_from_name("fin_funnel_2")
        fin3: LED = self._get_led_from_name("fin_funnel_3")
        fin4: LED = self._get_led_from_name("fin_funnel_4")
        fin5: LED = self._get_led_from_name("fin_funnel_5")
        fin6: LED = self._get_led_from_name("fin_funnel_6")

        LEDEffects.fire(fin1)
        LEDEffects.fire(fin2)
        LEDEffects.fire(fin3)
        LEDEffects.fire(fin4)
        LEDEffects.fire(fin5)
        LEDEffects.fire(fin6)

        return Response("finished", 200)
