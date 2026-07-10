"""
Tests that run the production code against VirtualHardware — no Pico needed.
"""
import asyncio

from src.gunpla.generic_gundam import GenericGundam
from src.hardware import get_hardware
from src.hardware.VirtualHardware import VirtualHardware
from src.pi.disabled_LED import DisabledLED
from src.pi.led_effect import LEDEffects
from src.server.lightshow_manager import LightshowManager
from src.server.Wrappers import create_show_handler


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
    def __init__(self):
        self.all_off_calls = 0

    def all_off(self):
        self.all_off_calls += 1


def test_lightshow_lifecycle_tracks_status():
    manager = LightshowManager(FakeGunpla())

    async def scenario():
        assert manager.status()["state"] == "idle"
        started = asyncio.Event()

        async def show():
            started.set()
            await asyncio.sleep(60)

        handler = create_show_handler("Marathon", show, manager)
        body, status = await handler(None)
        assert status == 202
        assert body["show"] == "Marathon"
        await started.wait()
        assert manager.is_running()
        assert manager.status() == {"state": "running", "show": "Marathon", "error": None}

        assert await manager.stop() == "Marathon"
        assert not manager.is_running()
        assert manager.status()["state"] == "stopped"
        assert await manager.stop() is None

    asyncio.run(scenario())


def test_show_outcomes_are_recorded():
    manager = LightshowManager(FakeGunpla())

    async def scenario():
        async def quick():
            pass

        await manager.start("Quick", quick)
        while manager.is_running():
            await asyncio.sleep(0)
        assert manager.status() == {"state": "completed", "show": "Quick", "error": None}

        async def bad():
            raise RuntimeError("boom")

        await manager.start("Bad", bad)
        while manager.is_running():
            await asyncio.sleep(0)
        assert manager.status() == {"state": "errored", "show": "Bad", "error": "boom"}

    asyncio.run(scenario())


def test_manual_action_cancels_show_and_records_finished():
    gunpla = FakeGunpla()
    manager = LightshowManager(gunpla)
    actions = []

    async def scenario():
        async def show():
            await asyncio.sleep(60)

        await manager.start("Marathon", show)
        await asyncio.sleep(0)
        await manager.run_action("All LEDs on", lambda: actions.append("all_on"))
        assert actions == ["all_on"]
        assert not manager.is_running()
        assert manager.status() == {"state": "finished", "show": "All LEDs on", "error": None}
        assert gunpla.all_off_calls == 1  # the cancelled show's LEDs were cleared first

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
        await manager.start("first", make_show("first"))
        await asyncio.sleep(0)
        # Two replacement requests land while the first show is still being
        # cancelled — without serialization one of these orphaned a show.
        await asyncio.gather(manager.start("second", make_show("second")),
                             manager.start("third", make_show("third")))
        await asyncio.sleep(0)
        assert running == ["third"]
        assert manager.is_running()
        assert manager.status()["show"] == "third"

        await manager.stop()
        assert running == []
        assert not manager.is_running()

    asyncio.run(scenario())
