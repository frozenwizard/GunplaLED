import asyncio

# Status states reported to the UI (MicroPython has no enum module)
IDLE = "idle"            # nothing has run yet
RUNNING = "running"      # a lightshow is currently running
COMPLETED = "completed"  # the last lightshow ran to its natural end
STOPPED = "stopped"      # the last lightshow was cancelled by the user or replaced
ERRORED = "errored"      # the last lightshow raised an exception
FINISHED = "finished"    # the last activity was a one-shot action like "All LEDs on"


class LightshowManager:
    """
    Owns the single running lightshow task for a gunpla and the status shown in
    the UI.  start/stop/run_action are serialized with a lock so overlapping
    requests can't orphan a running show or leave two shows fighting over the
    same LEDs.  Each show runs under a supervisor coroutine that records how it
    ended (completed, stopped, or errored) — outcomes MicroPython's Task object
    can't report on its own.
    """

    def __init__(self, gunpla):
        self.gunpla = gunpla
        self._task = None
        self._lock = asyncio.Lock()
        self._state = IDLE
        self._show = None
        self._error = None

    def status(self) -> dict:
        """
        :return: the current status as a dict, suitable for JSON responses
        """
        return {"state": self._state, "show": self._show, "error": self._error}

    def describe(self) -> str:
        """
        :return: a human readable one-liner of the current status for the UI
        """
        if self._state == IDLE:
            return "No lightshow has run yet."
        if self._state == RUNNING:
            return f"Lightshow '{self._show}' is running."
        if self._state == COMPLETED:
            return f"Lightshow '{self._show}' completed."
        if self._state == STOPPED:
            return f"Lightshow '{self._show}' was stopped."
        if self._state == ERRORED:
            return f"Lightshow '{self._show}' failed: {self._error}"
        return f"{self._show} — finished."

    def is_running(self) -> bool:
        """
        :return: True if a lightshow is currently running, False otherwise
        """
        return self._task is not None and not self._task.done()

    async def start(self, name: str, func) -> None:
        """
        Cancels any running show (turning the LEDs off), then starts func as
        the tracked lightshow task under a supervisor that records its outcome.
        """
        async with self._lock:
            await self._cancel_current()
            self._set_status(RUNNING, name)
            self._task = asyncio.create_task(self._supervise(name, func))

    async def stop(self):
        """
        Cancels any running lightshow, waits for it to clean up and turns the
        LEDs off.
        :return: the name of the cancelled show, or None if nothing was running
        """
        async with self._lock:
            return await self._cancel_current()

    async def run_action(self, description: str, action) -> None:
        """
        Runs a one-shot LED action (e.g. "All LEDs on"), cancelling any running
        show first so the show can't fight the user over the LEDs.
        :param description: what the action is, shown in the UI status
        :param action: a plain callable that manipulates the LEDs
        """
        async with self._lock:
            await self._cancel_current()
            action()
            self._set_status(FINISHED, description)

    def _set_status(self, state: str, show: str, error: str = None) -> None:
        self._state = state
        self._show = show
        self._error = error

    async def _supervise(self, name: str, func) -> None:
        try:
            await func()
        except asyncio.CancelledError:
            self._set_status(STOPPED, name)
            raise
        except Exception as e:
            print(f"Lightshow '{name}' failed: {e}")
            self._set_status(ERRORED, name, str(e))
        else:
            self._set_status(COMPLETED, name)

    async def _cancel_current(self):
        """
        Cancels the tracked show if one is still running, waits for its cleanup
        and turns all LEDs off.  Callers must hold the lock.
        :return: the name of the cancelled show, or None if nothing was running
        """
        task = self._task
        self._task = None
        if task is None or task.done():
            return None
        name = self._show
        task.cancel()
        try:
            await task  # Wait for cleanup; the supervisor records the outcome
        except asyncio.CancelledError:
            pass
        self.gunpla.all_off()
        return name
