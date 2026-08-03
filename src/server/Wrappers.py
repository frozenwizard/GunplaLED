from src.server.RouteDecorator import lightshow_route


def safe_execution(func):
    """
    Wraps an async route handler with a try/except block.
    Returns 500 on failure, passes through success.
    """

    async def wrapper(*args, **kwargs):
        try:
            print(f"Trying to execute {func.__name__}")
            result = await func(*args, **kwargs)
            # If the function returns a value, use it; otherwise return success JSON
            if result is not None:
                return result
            return {"status": "success", "action": func.__name__}, 202
        except Exception as e:
            # Log the error to console
            print(f"Server Error in {func.__name__}: {e}")
            return {"error": str(e)}, 500

    return wrapper


def create_show_handler(func, show_manager):
    """
    Helper that when given a function, wraps it as a lighthow_route and safe_execution.
    :param show_manager: the LightshowManager that owns the running show
    if needed we can add back in the request obj to show_handler and func(request)
    :param func:
    :return:
    """
    # note order matters for these
    @lightshow_route(show_manager)
    @safe_execution
    async def show_handler():
        return await func()

    return show_handler
