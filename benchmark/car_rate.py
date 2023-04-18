from base import BaseBenchmark, Rates
from config import BASE_RATE


def mono_car_rate(benchmark: BaseBenchmark):
    benchmark.rates.append(Rates(1, BASE_RATE))


def linear_car_rate(benchmark: BaseBenchmark, level_count: int, step: int = 0.3*BASE_RATE):
    for level in range(level_count):
        benchmark.rates.append(
            Rates((level+1), int(BASE_RATE+level*step)))


def exponential_car_rate(benchmark: BaseBenchmark, level_count: int, base=1.1):
    for level in range(level_count):
        benchmark.rates.append(
            Rates((level+1), int(BASE_RATE*(base**level)))
        )
