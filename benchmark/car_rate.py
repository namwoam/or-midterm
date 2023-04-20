from base import BaseBenchmark, Rates
from config import BASE_RATE


def mono_car_rate(benchmark: BaseBenchmark):
    assert benchmark.n_L == 1
    benchmark.rates.append(Rates(1, BASE_RATE))


def linear_car_rate(benchmark: BaseBenchmark, step: int = 0.3*BASE_RATE):
    level_count = benchmark.n_L
    for level in range(level_count):
        benchmark.rates.append(
            Rates((level+1), int(BASE_RATE+level*step)))


def exponential_car_rate(benchmark: BaseBenchmark, base=1.1, step: int = 1):
    level_count = benchmark.n_L
    for level in range(level_count):
        benchmark.rates.append(
            Rates((level+1), int(BASE_RATE*(base**(level*step))))
        )
