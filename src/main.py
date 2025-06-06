from q2_memory import q2_memory

from utils.profilers import mem_profiler, time_profiler

mem_usage = {}
time_usage = {}
file = "farmers-protest-tweets-2021-2-4.json"


def run_function(func, tag, file):
    @time_profiler(time_map=time_usage, tag=tag)
    @mem_profiler(mem_map=mem_usage, tag=tag)
    def wrapper(file):
        return func(file)

    return wrapper(file)


def main():
    run_function(
        lambda x: print(q2_memory(x)),
        "q2_memory",
        file,
    )

if __name__ == "__main__":
    main()
