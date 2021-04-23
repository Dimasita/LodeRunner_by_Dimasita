import time


def benchmark(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        print(f'Время выполнения: {end - start} секунд.')
        return return_value
    return wrapper
