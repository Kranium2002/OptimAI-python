"""This module contains the optimize decorator for
optimizing Python functions using LLMs and performance
profiling."""
import os
import inspect
import functools
from io import StringIO
from contextlib import redirect_stdout
from perfwatch import watch
from optimizeai.llm_wrapper import LLMWrapper
from optimizeai.config import Config

def get_function_code(func):
    """Get the source code of a function if it's defined in the current directory."""
    try:
        source_lines, _ = inspect.getsourcelines(func)
        source_file = inspect.getfile(func)
        current_directory = os.path.dirname(os.path.abspath(__file__))
        if source_file.startswith(current_directory):
            return ''.join(source_lines)
    except (TypeError, OSError):
        return None

def optimize(profiler_types, config: Config):
    """Decorator to optimize a Python function using LLMs and performance profiling."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Capture the executed code
            code_lines, _ = inspect.getsourcelines(func)
            code = ''.join(code_lines[1:])  # Remove the decorator line

            # Find and include the code of all called functions
            called_functions = inspect.getmembers(func, predicate=inspect.isfunction)
            for name, called_func in called_functions:
                func_code = get_function_code(called_func)
                if func_code:
                    code += f'\n\n# Function {name}\n' + func_code

            # Profile the function and capture the output
            with StringIO() as buf, redirect_stdout(buf):
                watch(profiler_types)(func)(*args, **kwargs)
                captured_output = buf.getvalue()

            # Initialize the LLMWrapper with the provided config
            llm_wrapper = LLMWrapper(config)
            response = llm_wrapper.send_request(code=code, perf_metrics=captured_output)

            print(response)
            return response

        return wrapper
    return decorator


