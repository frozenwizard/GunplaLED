import asyncio


def lightshow_route(app, manager_attr="current_task"):
    """
    A decorator factory that handles task management and
    standardized HTTP responses.
    """
    def decorator(func):
        async def wrapper(self, request, *args, **kwargs):
            # 1. Kill any existing show to prevent flickering/overlap
            existing_task = getattr(self, manager_attr, None)
            if existing_task and not existing_task.done():
                existing_task.cancel()
                try:
                    #TODO: turn all leds off
                    await existing_task  # Wait for cleanup
                except asyncio.CancelledError:
                    pass

            # 2. Start the new show and track it
            # We wrap the function call to ensure we catch the 'self' instance
            task = asyncio.create_task(func(self, request, *args, **kwargs))
            setattr(self, manager_attr, task)

            # 3. Standardized Response
            return {
                "status": "started",
                "show": func.__name__,
                # "message": "Gundam sequence initiated"
            }, 202
        return wrapper
    return decorator
