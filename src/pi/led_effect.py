import asyncio
import time

from machine import PWM

from src.pi import LED


class LEDEffects:
    """
    A collection of effects a LED can do.  Things such as pulsate, breath, flash, etc.
    """

    @staticmethod
    async def blink(led: LED) -> None:
        """
        Blinks the onboard LED twice
        """
        led.on()
        time.sleep(0.5)
        led.off()
        await asyncio.sleep(0.5)
        led.on()
        await asyncio.sleep(0.5)
        led.off()

    @staticmethod
    async def fire(led: LED) -> None:
        """
        A simple weapon effect of firing a beam rifle, has no charging effect
        :param led:
        :return:
        """
        led.on()
        await asyncio.sleep(.5)
        led.off()

    @staticmethod
    async def charge_fire(led: LED, charge_speed: int = 1) -> None:
        """
        A simple charging of a shot
        """
        await LEDEffects.brighten(led, start_percent=0, end_percent=75, speed=charge_speed)
        led.off()
        await asyncio.sleep(0.5)
        # LEDEffects.brighten(led, start_percent=75, end_percent=100, speed=1)
        led.on()
        await asyncio.sleep(2)
        led.off()

    @staticmethod
    async def brighten(led: LED, start_percent: int = 0, end_percent: int = 100, speed: int = 10) -> None:
        """
        Starting from start_pct goes to end_pct over the course of speed, brightens led
        :param led:
        :param end_percent:
        :param start_percent:
        :param speed:
        :return:
        """

        pwm = PWM(led.pin)
        pwm.freq(1000)
        step_rate = 10

        overall_change = end_percent - start_percent
        interval = overall_change / step_rate
        sleep_time = speed / interval
        # print(f"overall[{overall_change}] interval[{interval}] sleep[{sleep_time}]")
        # todo: use interval as the loop counter and just increment percent until end_percent
        for percent in range(start_percent, end_percent, step_rate):
            duty = int((percent / 100) * 65_535)
            pwm.duty_u16(duty)
            await asyncio.sleep(sleep_time)
        pwm.deinit()

    @staticmethod
    async def brighten_all(leds: list[LED], start_percent: int = 0, end_percent: int = 100, speed: int = 10) -> None:
        """
        The current banshee amount of leds passed in causes it to I guess stack overflow and silently crash
        around 30%  so this method should not be used until that's addressed.
        """
        pwms = []
        for led in leds:
            pwm = PWM(led.pin)
            pwm.freq(1000)
            pwms.append(pwm)

        step_rate = 10

        overall_change = end_percent - start_percent
        interval = overall_change / step_rate
        sleep_time = speed / interval

        for percent in range(start_percent, end_percent, step_rate):
            print(percent)
            duty = int((percent / 100) * 65_535)
            for pwm in pwms:
                pwm.duty_u16(duty)
            await asyncio.sleep(sleep_time)

        for pwm in pwms:
            pwm.deinit()
