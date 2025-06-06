import io
import memray
from memory_profiler import profile as mem_profile
from memory_profiler import memory_usage
import cProfile
import pstats
from typing import Callable, Any
import uuid

def mem_profiler2(mem_map: dict, tag: str) -> Callable[..., Any]:
    """
    A decorator factory that profiles the memory usage of a given function.

    Args:
        mem_map (dict): A dictionary to store the memory profile results.
        tag (str): A tag to identify the memory profile result in the mem_map.

    Returns:
        Callable[..., Any]: A decorator that profiles the memory usage of a function.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs):
            code = uuid.uuid4()
            with memray.Tracker(f"mem_profile_{code}.bin"):
                result = func(*args, **kwargs)
            data = []
            with memray.FileReader(f"mem_profile_{code}.bin") as reader:
                for record in reader.get_memory_snapshots():
                    item = [record.time, record.rss, record.heap]
                    data.append(item)
            # delete the file after reading
            import os
            os.remove(f"mem_profile_{code}.bin")
            mem_map[tag] = data
            return result
        return wrapper
    return decorator

def mem_profiler(mem_map: dict, tag: str) -> Callable[..., Any]:
    """
    A decorator factory that profiles the memory usage of a given function.

    Args:
        mem_map (dict): A dictionary to store the memory profile results.
        tag (str): A tag to identify the memory profile result in the mem_map.

    Returns:
        Callable[..., Any]: A decorator that profiles the memory usage of a function.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs):
            mem_result = []
            # Baseline mem profile
            with io.StringIO() as buffer:
                @mem_profile(stream=buffer)
                def start_func():
                    pass  # placeholder to know memory usage at the start
                start_func()
                mem_result.append(parse_memory_profile(buffer.getvalue()))
            # Function mem profile
            with io.StringIO() as buffer:
                result = None
                @mem_profile(stream=buffer)
                def run_func():
                    return func(*args, **kwargs)
                result = run_func()
                mem_result.append(parse_memory_profile(buffer.getvalue()))
                mem_map[tag] = mem_result
            return result
        return wrapper
    return decorator

def parse_memory_profile(mem_profile_str: str) -> dict:
    """
    Parses the memory profile string and extracts relevant data.
    Args:
        mem_profile_str (str): The memory profile string to parse.
    Returns:
        dict: List of elements within the table output (only the one with memories).
    """
    data = []
    for line in mem_profile_str.split("\n"):
        items = [w.strip() for w in line.split("  ") if len(w) > 0 and not w.strip().startswith("#")]
        if len(items) > 2:
            data.append(items)
    return data

def time_profiler(time_map: dict, tag: str) -> Callable[..., Any]:
    """
    A decorator factory that profiles the execution time of a given function.

    Args:
        time_map (dict): A dictionary to store the profiling results.
        tag (str): A tag to identify the profiling result in the time_map.

    Returns:
        Callable[..., Any]: A decorator that profiles the execution time of a function.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs):
            with cProfile.Profile() as pr:
                result = func(*args, **kwargs)
                string_io = io.StringIO()
                pstats.Stats(pr, stream=string_io).strip_dirs().sort_stats("cumulative").print_stats()
                time_map[tag] = string_io.getvalue()
            return result
        return wrapper
    return decorator
