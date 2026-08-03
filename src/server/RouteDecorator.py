import asyncio


def is_lightshow_running(gunpla, manager_attr="current_task") -> bool:
    """
    :return: True if a lightshow task is currently tracked and hasn't finished yet
    """
    existing_task = getattr(gunpla, manager_attr, None)
    return existing_task is not None and not existing_task.done()


async def cancel_lightshow(gunpla, manager_attr="current_task"):
    """
    Cancels any running lightshow task on the gunpla and clears the tracked task.
    Callers must hold gunpla.lightshow_lock: this check-then-act sequence needs to stay
    atomic with respect to other requests reading/writing the tracked task.
    :return: True if a running show was cancelled, False if nothing was running
    """
    existing_task = getattr(gunpla, manager_attr, None)
    if is_lightshow_running(gunpla, manager_attr):
        existing_task.cancel()
        try:
            await existing_task  # Wait for cleanup
        except asyncio.CancelledError:
            pass
        setattr(gunpla, manager_attr, None)
        return True
    setattr(gunpla, manager_attr, None)
    return False


def lightshow_route(gunpla, manager_attr="current_task"):
    """
    A decorator factory that handles task management and
    standardized HTTP responses.
    """
    def decorator(func):
        async def wrapper(request, *args, **kwargs):
            async with gunpla.lightshow_lock:
                # If any existing lightshow is running, cancel it and turn off all the LEDs.
                if await cancel_lightshow(gunpla, manager_attr):
                    gunpla.all_off()

                # Start the new show and track it
                task = asyncio.create_task(func())
                setattr(gunpla, manager_attr, task)

            # Return common HTTP response that the show started.
            return {
                "status": "started",
                "show": func.__name__,
            }, 202
        return wrapper
    return decorator
