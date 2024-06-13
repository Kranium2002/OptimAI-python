"""This module contains the optimize decorator for
optimizing Python functions using LLMs and performance
profiling."""
import inspect
import functools
from io import StringIO
import sys
from perfwatch import watch
from optimizeai.llm_wrapper import LLMWrapper
from optimizeai.config import Config

# Define a context manager to capture stdout
class CapturingStringIO(StringIO):
    """Context manager to capture stdout."""
    def __init__(self):
        super().__init__()
        self._stdout = None        
    
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self._stdout
        if exc_type is not None:
            return False
        return True

# Custom optimize decorator
def optimize(profiler_types, config: Config):
    """Decorator to optimize a Python function using LLMs and performance profiling."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Capture the executed code
            code = inspect.getsource(func)

            # Profile the function and capture the output
            with CapturingStringIO() as stdout:
                results = watch(profiler_types)(func)(*args, **kwargs)
                captured_output = stdout.getvalue()
            
            # Get the function output and metrics
            func_output = results[0][1] if results else None
            metrics = "\n".join([f"{ptype}: {result}" for ptype, result in results])
            
            # Initialize the LLMWrapper with the provided config
            llm_wrapper = LLMWrapper(config)
            
            # Send metrics, captured output, and code to LLM
            prompt = f"""
            Optimize the following Python function for better performance and efficiency in short conscise way:

            ---

            Function Code:
            {code}

            ---

            Output Produced:
            {captured_output}

            ---

            Performance Metrics:
            {metrics}

            ---

            Optimize the function to reduce execution time, memory usage, and improve overall efficiency. Provide short detailed technical tips and refactor suggestions, such as algorithm improvements, data structure optimizations, or parallelization strategies.
            """
            
            response = llm_wrapper.send_request(prompt)
            
            print(response)
            
            return func_output
        
        return wrapper
    return decorator
