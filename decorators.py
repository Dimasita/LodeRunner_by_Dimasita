import time


def benchmark(i: int = 1):
    def decor(func):
        def wrapper(*args, **kwargs):
            min_time = 0
            max_time = 0
            total_time = 0
            for j in range(i):
                start = time.time()
                return_value = func(*args, **kwargs)
                end = time.time()
                single_time = end - start

                if j == 0:
                    min_time = single_time
                    max_time = single_time
                else:
                    if min_time > single_time:
                        min_time = single_time
                    if max_time < single_time:
                        max_time = single_time

                total_time += single_time
            if i == 1:
                print(f'Время выполнения: {min_time} секунд.')
            else:
                print(f'Min время выполнения: {min_time} секунд.')
                print(f'Avg время выполнения: {total_time / i} секунд ({i} iterations).')
                print(f'Max время выполнения: {max_time} секунд.')

            return return_value
        return wrapper
    return decor
