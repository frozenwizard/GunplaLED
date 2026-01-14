import json

from src.pi.disabled_LED import DisabledLED
from src.pi.LED import LED
from src.server.Wrappers import safe_execution


class BaseGundam:
    """
    Base Gunpla.
    """

    def __init__(self, hardware):
        from src.hardware.Hardware import Hardware
        self.hardware: Hardware = hardware
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
        self._all_leds_on()

    def _all_leds_on(self) -> str:
        """
        Turns all LEDs on
        """
        leds: str = ""
        for led_entry in self.config['leds']:
            led_name = led_entry['name']
            led = self._get_led_from_name(led_name)
            led.on()
            if isinstance(led, DisabledLED):
                leds += f"{led_name}: disabled\n"
            else:
                leds += f"{led_name}: on\n"
        return leds

    def all_off(self) -> None:
        """
        Turns all configured LED's off
        """
        print("turning off all leds")
        self._all_leds_off()

    def _all_leds_off(self) -> str:
        """"
        Turns all LEDs off
        """
        leds: str = ""
        for led_entry in self.config['leds']:
            led_name = led_entry['name']
            led = self._get_led_from_name(led_name)
            led.off()
            if isinstance(led, DisabledLED):
                leds += f"{led_name}: disabled\n"
            else:
                leds += f"{led_name}: off\n"
        return leds

    def get_all_leds(self, ignore_list: list[str] = []) -> list[LED]:
        """
        Returns all LEDs configured, enabled or disabled.  But not the board_led
        """
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
        Given a name of an LED, returns the LED object for it.
        Throws an exception if it's not found
        :param led_name:
        :return:
        """
        entry = self.__get_entry_from_name(led_name)
        if 'disabled' in entry and entry['disabled']:
            print(f"{led_name} is disabled")
            return DisabledLED(led_name)
        return self.hardware.create_led(entry['pin'], led_name)

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
