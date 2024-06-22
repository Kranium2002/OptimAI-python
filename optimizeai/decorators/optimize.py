"""This module contains the optimize decorator for
optimizing Python functions using LLMs and performance
profiling."""
import inspect
import functools
from io import StringIO
from contextlib import redirect_stdout
from perfwatch import watch
from optimizeai.llm_wrapper import LLMWrapper
from optimizeai.config import Config

# Custom optimize decorator
def optimize(profiler_types, config: Config):
    """Decorator to optimize a Python function using LLMs and performance profiling."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Capture the executed code
            source_lines, _ = inspect.getsourcelines(func)
            # Remove the first line (which is the decorator line)
            code = ''.join(source_lines[1:])

            # Profile the function and capture the output
            with StringIO() as buf, redirect_stdout(buf):
                watch(profiler_types)(func)(*args, **kwargs)
                captured_output = buf.getvalue()

            # Initialize the LLMWrapper with the provided config
            llm_wrapper = LLMWrapper(config)
            response= llm_wrapper.send_request(code = code, perf_metrics=captured_output)

            print(response)
            return response

        return wrapper
    return decorator
