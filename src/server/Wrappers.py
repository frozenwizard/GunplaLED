from src.server.RouteDecorator import lightshow_route


def safe_execution(func):
    """
    Wraps an async route handler with a try/except block.
    Returns 500 on failure, passes through success.
    """

    async def wrapper(*args, **kwargs):
        try:
            print(f"Trying to execute {func.__name__}")
            await func(*args, **kwargs)
            return {"status": "success", "action": func.__name__}, 202
        except Exception as e:
            # Log the error to console
            print(f"Server Error in {func.__name__}: {e}")
            return {"error": str(e)}, 500

    return wrapper


def create_show_handler(func, gundam_instance):
    """
    Helper that when given a function, wraps it as a lighthow_route and safe_execution.
    :param gundam_instance:
    if needed we can add back in the request obj to show_handler and func(request)
    :param func:
    :return:
    """
    # note order matters for these
    @lightshow_route(gunpla=gundam_instance)
    @safe_execution
    async def show_handler():
        return await func()

    return show_handler
