import asyncio

from src.gunpla.base_gundam import BaseGundam
from src.pi.led_effect import LEDEffects


class UnicornBansheeGundam(BaseGundam):
    """
    RX-0 Unicorn Gundam 02 Banshee(https://gundam.fandom.com/wiki/RX-0_Unicorn_Gundam_02_Banshee)
    """

    def get_config_file(self) -> str:
        """
        :return: The Unicorn Banshee Gundam config file
        """
        return "src/config/unicorn_banshee.json"

    async def glow(self) -> None:
        """
        Runs the glow lightshow
        """
        await LEDEffects.brighten_all(self.get_all_leds())
        await asyncio.sleep(3)
        self._all_leds_off()
