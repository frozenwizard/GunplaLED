import uasyncio


def lightshow_route(gunpla, manager_attr="current_task"):
    """
    A decorator factory that handles task management and
    standardized HTTP responses.
    """
    def decorator(func):
        async def wrapper(request, *args, **kwargs):
            # If any existing lightshow is running, cancel it and turn off all the LEDs.
            existing_task = getattr(gunpla, manager_attr, None)
            if existing_task and not existing_task.done():
                existing_task.cancel()
                try:
                    gunpla.all_off()
                    await existing_task  # Wait for cleanup
                except uasyncio.CancelledError:
                    pass

            # Start the new show and track it
            task = uasyncio.create_task(func())
            setattr(gunpla, manager_attr, task)

            # Return common HTTP response that the show started.
            return {
                "status": "started",
                "show": func.__name__,
            }, 202
        return wrapper
    return decorator
