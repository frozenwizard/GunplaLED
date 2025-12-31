from src.server.RouteDecorator import lightshow_route


def safe_execution(func):
    """
    Wraps an async route handler with a try/except block.
    Returns 500 on failure, passes through success.
    """

    async def wrapper(*args, **kwargs):
        try:
            await func(*args, **kwargs)
            return {"status": "success", "action": func.__name__}, 202

        except Exception as e:
            # Log the error to console (essential for debugging)
            print(f"Server Error in {func.__name__}: {e}")
            return {"error": str(e)}, 500

    return wrapper


def create_show_handler(func):
    """
    Given a function, wraps it as a lighthow_route and safe_execution.
    :param func:
    :return:
    """
    # note order matters for these
    @lightshow_route
    @safe_execution
    async def show_handler(request):
        return await func(request)

    return show_handler
