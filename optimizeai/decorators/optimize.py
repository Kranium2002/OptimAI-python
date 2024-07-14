"""This module contains the optimize decorator for
optimizing Python functions using LLMs and performance
profiling."""
from optimizeai.llm_wrapper import LLMWrapper
from optimizeai.pdf_utils import create_pdf_report
from optimizeai.config import Config
import types
import inspect
import functools
from io import StringIO
from contextlib import redirect_stdout
import sys
import datetime
import os
if not os.path.exists("logs"):
    os.makedirs("logs")
formatted_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.environ['LOG_FILE_PATH'] = f"logs/{formatted_datetime}.log"

from perfwatch import watch

def get_function_code(func):
    """Retrieve the source code of a function."""
    try:
        source_lines, _ = inspect.getsourcelines(func)
        return ''.join(source_lines)
    except (IOError, TypeError):
        return f"Source code not available for {func.__name__}"

def is_user_defined_function(func, base_folder):
    """Check if a function is user-defined."""
    if isinstance(func, types.FunctionType):
        func_file = inspect.getfile(func)
        # Check if the function file path starts with the base folder path
        return func_file.startswith(base_folder)
    return False

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
                # Create a dictionary to store called functions' source codes
                called_funcs_code = {}

                def trace_calls(frame, event, arg):
                    if event == 'call':
                        called_func = frame.f_globals.get(frame.f_code.co_name)
                        base_folder = os.path.dirname(inspect.getfile(func))
                        if is_user_defined_function(called_func, base_folder):
                            called_funcs_code[frame.f_code.co_name] = get_function_code(called_func)
                    return trace_calls

                # Set the trace function
                sys.settrace(trace_calls)

                try:
                    watch(profiler_types)(func)(*args, **kwargs)
                finally:
                    # Remove the trace function
                    sys.settrace(None)
                
                captured_output = buf.getvalue()
            captured_logs = str(open(os.getenv("LOG_FILE_PATH"), "r", encoding="utf-8").read())
            captured_output += captured_logs

            # Initialize the LLMWrapper with the provided config
            llm_wrapper = LLMWrapper(config)
            response = llm_wrapper.send_request(code=str(code), context=str(list(called_funcs_code.values())[1:]), perf_metrics=captured_output)
            print(response)

            # Create a PDF report from the response
            pdf_path = f"logs/report_{formatted_datetime}.pdf"
            create_pdf_report(response, pdf_path)

            return response

        return wrapper
    return decorator
