from base import BaseBenchmark

from random import randint, choice


def random_start_site(benchmark: BaseBenchmark):
    station_count = benchmark.distance.station_count
    for car in benchmark.cars:
        car.initial_station = randint(1, station_count)


def random_center_start_site(benchmark: BaseBenchmark, center_count=-1):
    station_count = benchmark.n_S
    if center_count == -1:
        center_count = max(1, station_count // 5)
    centers = [randint(1, station_count) for _ in range(center_count)]
    for car in benchmark.cars:
        car.initial_station = choice(centers)
