import time
import random

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

    def random_funnels(self, request: Request) -> Response:
        """
        Randomly fires fin funnels that are enabled for an infinite amount of time
        This currently does not end and needs thread management to properly be able to be halted.
        """
        funnels = [self._get_led_from_name("fin_funnel_1"), self._get_led_from_name("fin_funnel_2"),
                   self._get_led_from_name("fin_funnel_3"), self._get_led_from_name("fin_funnel_4"),
                   self._get_led_from_name("fin_funnel_5"), self._get_led_from_name("fin_funnel_6")]

        # Filter out funnels that are disabled.
        funnels = [funnel for funnel in funnels if funnel.enabled()]

        if not funnels:
            return Response("No funnels can be fired", 400)

        while True:
            funnel = random.choice(funnels)
            LEDEffects.fire(funnel)
            time.sleep(random.uniform(0, 3))

        return Response("finished", 200)
