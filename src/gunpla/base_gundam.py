import json

from src.pi.disabled_LED import DisabledLED
from src.pi.LED import LED
from src.pi.led_effect import LEDEffects


class BaseGundam:
    """
    Base Gunpla.
    """

    def __init__(self, hardware, config: dict = None):
        """
        :param hardware: The hardware abstraction to drive LEDs with.
        :param config: An in-memory config to use instead of reading get_config_file() from disk.
        """
        from src.hardware.Hardware import Hardware
        self.hardware: Hardware = hardware
        self.effects = LEDEffects(hardware)
        self._leds = {}
        if config is not None:
            self.config: json = config
        else:
            with open(self.get_config_file()) as config_contents:
                self.config: json = json.loads(config_contents.read())

    def get_config_file(self) -> str:
        """
        Returns the path to the corresponding Gundam json file
        This is abstract
        """
        raise Exception("Not implemented")

    def led_on(self, led_name: str):
        """
        Turns a Single LED on by name
        """
        print(f"turning on {led_name}")
        led = self._get_led_from_name(led_name)
        led.on()

    def led_off(self,  led_name: str) -> None:
        """
        Turns a single LED off by name
        """
        print(f"turning off {led_name}")
        led = self._get_led_from_name(led_name)
        led.off()

    def all_on(self) -> None:
        """
        Turns all configured LED's on.
        """
        print("turning on all leds")
        for led in self.get_all_leds():
            led.on()

    def all_off(self) -> None:
        """
        Turns all configured LED's off
        """
        print("turning off all leds")
        for led in self.get_all_leds():
            led.off()

    def get_all_leds(self, ignore_list: list[str] = None) -> list[LED]:
        """
        Returns all LEDs configured, enabled or disabled.  But not the board_led
        """
        ignore_list = ignore_list or []
        leds = []
        for led_entry in self.config['leds']:
            led_name = led_entry['name']
            if led_name in ignore_list:
                continue
            led = self._get_led_from_name(led_name)
            leds.append(led)
        return leds

    def _get_led_from_name(self, led_name: str) -> LED:
        """
        Given a name of an LED, returns the LED object for it, creating and caching it on first use.
        Throws an exception if it's not found
        :param led_name:
        :return:
        """
        led = self._leds.get(led_name)
        if led is None:
            entry = self.__get_entry_from_name(led_name)
            if 'disabled' in entry and entry['disabled']:
                print(f"{led_name} is disabled")
                led = DisabledLED(led_name)
            else:
                led = self.hardware.create_led(entry['pin'], led_name)
            self._leds[led_name] = led
        return led

    def __get_entry_from_name(self, led_name: str) -> json:
        """
        Given an LED name, returns the corresponding JSON config entry for it.
        :param led_name:
        :return:
        """
        for entry in self.config['leds']:
            if entry['name'] == led_name:
                return entry
        raise Exception(f"Entry '{led_name}' not found")
