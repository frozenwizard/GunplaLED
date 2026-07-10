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


def create_show_handler(name, func, show_manager):
    """
    Builds a route handler that starts func as the named lightshow through the
    show manager.  Errors inside the running show itself are recorded by the
    manager's supervisor, not here — safe_execution only guards the request.
    :param name: the lightshow name from the model config, shown in the UI
    :param func: the async lightshow method on the gunpla
    :param show_manager: the LightshowManager that owns the running show
    :return:
    """
    @safe_execution
    async def show_handler(request):
        await show_manager.start(name, func)
        return {"status": "started", "show": name}, 202

    return show_handler
