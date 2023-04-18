from base import BaseBenchmark
from config import MAP_SIZE

from random import randint
from math import sqrt


def random_station(benchmark: BaseBenchmark):
    station_count = benchmark.distance.station_count
    for station_index in station_count:
        benchmark.distance.stations[station_index] = (
            randint(0, MAP_SIZE-1), randint(0, MAP_SIZE-1))
