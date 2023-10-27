import time
from functools import wraps


def backoff(
    start_sleep_time: float = 0.1,
    factor: int = 2,
    border_sleep_time: int = 10,
    max_iterations: int = 10,
    exceptions: list[Exception] = [],
):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * (factor ^ n), если t < border_sleep_time
        t = border_sleep_time, иначе
    :param exceptions: список исключений
    :param max_iterations:  максимальное число повторений
    :param start_sleep_time: начальное время ожидания
    :param factor: во сколько раз нужно увеличивать время ожидания на каждой итерации
    :param border_sleep_time: максимальное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            iteration = 0
            while iteration <= max_iterations:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    sleep_time = start_sleep_time * factor**iteration
                    if sleep_time > border_sleep_time:
                        sleep_time = border_sleep_time
                    time.sleep(sleep_time)
                    iteration += 1

        return inner

    return func_wrapper
