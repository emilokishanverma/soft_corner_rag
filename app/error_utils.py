import inspect


def get_error_context() -> dict:
    frame = inspect.currentframe()

    if frame is None or frame.f_back is None:
        return {
            "module": "unknown",
            "function": "unknown",
            "file_name": "unknown",
            "line_number": 0,
        }

    caller = frame.f_back.f_back if frame.f_back and frame.f_back.f_back else frame.f_back

    return {
        "module": caller.f_globals.get("__name__", "unknown"),
        "function": caller.f_code.co_name,
        "file_name": caller.f_code.co_filename,
        "line_number": caller.f_lineno,
    }


def raise_custom_error(exception_class, message: str, original_error: Exception):
    ctx = get_error_context()
    raise exception_class(
        message=message,
        module=ctx["module"],
        function=ctx["function"],
        file_name=ctx["file_name"],
        line_number=ctx["line_number"],
        original_error=original_error,
    )