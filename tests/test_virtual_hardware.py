"""
Tests that run the production code against VirtualHardware — no Pico needed.
"""
import asyncio

from src.gunpla.generic_gundam import GenericGundam
from src.hardware import get_hardware
from src.hardware.VirtualHardware import VirtualHardware
from src.pi.disabled_LED import DisabledLED
from src.pi.led_effect import LEDEffects
from src.server.RouteDecorator import LightshowManager, lightshow_route


def test_get_hardware_selects_virtual_off_device():
    assert isinstance(get_hardware(), VirtualHardware)


def test_board_led_is_the_real_class_with_a_mock_pin():
    hardware = VirtualHardware()
    led = hardware.board_led()
    assert led.name() == "Board LED"
    assert led.enabled()
    led.on()
    led.off()


def test_board_led_and_networking_are_cached_like_pico_hardware():
    hardware = VirtualHardware()
    assert hardware.board_led() is hardware.board_led()
    assert hardware.networking() is hardware.networking()


def test_brighten_drives_pwm_through_injected_hardware():
    hardware = VirtualHardware()
    led = hardware.create_led(5, "head")
    asyncio.run(LEDEffects(hardware).brighten(led, speed=0))


def test_brighten_with_equal_percentages_is_a_noop():
    hardware = VirtualHardware()
    led = hardware.create_led(5, "head")
    asyncio.run(LEDEffects(hardware).brighten(led, start_percent=50, end_percent=50))


def test_effects_skip_disabled_leds():
    hardware = VirtualHardware()
    effects = LEDEffects(hardware)
    asyncio.run(effects.brighten(DisabledLED("ghost")))
    asyncio.run(effects.brighten_all([hardware.create_led(1, "a"), DisabledLED("ghost")], speed=0))


def test_gundam_caches_led_objects():
    gundam = GenericGundam(VirtualHardware())
    assert gundam._get_led_from_name("head") is gundam._get_led_from_name("head")


def test_all_on_and_off_run_on_virtual_hardware():
    gundam = GenericGundam(VirtualHardware())
    gundam.all_on()
    gundam.all_off()


class FakeGunpla:
    def all_off(self):
        pass


def test_lightshow_lifecycle_tracks_and_clears_task():
    manager = LightshowManager(FakeGunpla())

    async def scenario():
        started = asyncio.Event()

        async def show():
            started.set()
            await asyncio.sleep(60)

        handler = lightshow_route(manager)(show)
        _, status = await handler(None)
        assert status == 202
        await started.wait()
        assert manager.is_running()

        assert await manager.stop() is True
        assert not manager.is_running()
        assert await manager.stop() is False

    asyncio.run(scenario())


def test_overlapping_start_requests_do_not_orphan_a_show():
    manager = LightshowManager(FakeGunpla())
    running = []

    def make_show(name):
        async def show():
            running.append(name)
            try:
                await asyncio.sleep(60)
            finally:
                running.remove(name)
        return show

    async def scenario():
        await manager.start(make_show("first"))
        await asyncio.sleep(0)
        # Two replacement requests land while the first show is still being
        # cancelled — without serialization one of these orphaned a show.
        await asyncio.gather(manager.start(make_show("second")), manager.start(make_show("third")))
        await asyncio.sleep(0)
        assert running == ["third"]
        assert manager.is_running()

        await manager.stop()
        assert running == []
        assert not manager.is_running()

    asyncio.run(scenario())
