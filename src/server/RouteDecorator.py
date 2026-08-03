import asyncio


class LightshowManager:
    """
    Owns the single running lightshow task for a gunpla.  start() and stop() are
    serialized with a lock so overlapping requests can't orphan a running show
    or leave two shows fighting over the same LEDs.
    """

    def __init__(self, gunpla):
        self.gunpla = gunpla
        self._task = None
        self._lock = asyncio.Lock()

    def is_running(self) -> bool:
        """
        :return: True if a lightshow is currently running, False otherwise
        """
        return self._task is not None and not self._task.done()

    async def start(self, func) -> None:
        """
        Cancels any running show (turning the LEDs off), then starts func as the
        tracked lightshow task.
        """
        async with self._lock:
            if await self._cancel_current():
                self.gunpla.all_off()
            self._task = asyncio.create_task(func())

    async def stop(self) -> bool:
        """
        Cancels any running lightshow and waits for it to clean up.
        :return: True if a running show was cancelled, False if nothing was running
        """
        async with self._lock:
            return await self._cancel_current()

    async def _cancel_current(self) -> bool:
        task = self._task
        self._task = None
        if task is None or task.done():
            return False
        task.cancel()
        try:
            await task  # Wait for cleanup
        except asyncio.CancelledError:
            pass
        except Exception as e:
            # A show that died on its own shouldn't fail the cancelling request
            print(f"Lightshow ended with error: {e}")
        return True


def lightshow_route(manager: LightshowManager):
    """
    A decorator factory that handles task management and
    standardized HTTP responses.
    """
    def decorator(func):
        async def wrapper(request, *args, **kwargs):
            # Replaces any running lightshow with this one.
            await manager.start(func)

            # Return common HTTP response that the show started.
            return {
                "status": "started",
                "show": func.__name__,
            }, 202
        return wrapper
    return decorator
