import uasyncio


def lightshow_route(gunpla, manager_attr="current_task"):
    """
    A decorator factory that handles task management and
    standardized HTTP responses.
    """
    def decorator(func):
        print("decorating route")

        async def wrapper(request, *args, **kwargs):
            print("wrapping route")
            # 1. Kill any existing show to prevent flickering/overlap
            existing_task = getattr(gunpla, manager_attr, None)
            if existing_task and not existing_task.done():
                existing_task.cancel()
                try:
                    gunpla.all_off()
                    await existing_task  # Wait for cleanup
                except uasyncio.CancelledError:
                    pass

            # 2. Start the new show and track it
            task = uasyncio.create_task(func())
            setattr(gunpla, manager_attr, task)

            # 3. Standardized Response
            return {
                "status": "started",
                "show": func.__name__,
                # "message": "Gundam sequence initiated"
            }, 202
        print("wappred route")
        return wrapper
    print("lighted route")
    return decorator
