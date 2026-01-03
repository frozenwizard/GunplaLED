import random

import asyncio

from src.gunpla.base_gundam import BaseGundam
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

    async def activation(self) -> None:
        """
        Runs the activation lightshow
        this is just a sample test
        """
        head_led = self._get_led_from_name("head")
        head_led.on()
        await asyncio.sleep(0.1)
        head_led.off()
        await asyncio.sleep(0.5)
        await LEDEffects.brighten(head_led)

    async def fire_funnels(self) -> None:
        """
        Light Show that fires fin funnels in order
        """
        for i in range(1, 7):
            funnel = self._get_led_from_name(f"fin_funnel_{i}")
            await LEDEffects.fire(funnel)

    async def random_funnels(self) -> None:
        """
        Randomly fires fin funnels that are enabled for an infinite amount of time
        This currently does not end and needs thread management to properly be able to be halted.
        """
        funnels = [self._get_led_from_name("fin_funnel_1"), self._get_led_from_name("fin_funnel_2"),
                   self._get_led_from_name("fin_funnel_3"), self._get_led_from_name("fin_funnel_4"),
                   self._get_led_from_name("fin_funnel_5"), self._get_led_from_name("fin_funnel_6")]

        # Filter out funnels that are disabled.
        funnels = [funnel for funnel in funnels if funnel.enabled()]

        while True:
            funnel = random.choice(funnels)
            await LEDEffects.charge_fire(funnel)
            await asyncio.sleep(random.uniform(0, 3))
