from base import BaseBenchmark, Car

from random import randint

import numpy as np


def random_car_level(benchmark: BaseBenchmark):
    car_count = benchmark.n_C
    level_count = benchmark.n_L
    for car_id in range(car_count):
        benchmark.cars.append(Car(car_id+1, randint(1, level_count)))


def middle_normal_car_level(benchmark: BaseBenchmark):
    car_count = benchmark.n_C
    level_count = benchmark.n_L
    levels = np.random.normal(level_count//2, level_count//2, size=(car_count))
    for index, level in enumerate(levels):
        if level < 1:
            levels[index] = 1
        elif level > level_count:
            levels[index] = level_count
    for car_id in range(car_count):
        benchmark.cars.append(
            Car(car_id+1, int(levels[car_id])))


def decreasing_normal_car_level(benchmark: BaseBenchmark):
    car_count = benchmark.n_C
    level_count = benchmark.n_L
    levels = np.abs(np.random.normal(0, level_count, size=(car_count)))
    for index, level in enumerate(levels):
        if level < 1:
            levels[index] = 1
        elif level > level_count:
            levels[index] = level_count
    for car_id in car_count:
        benchmark.cars.append(
            Car(car_id+1, int(levels[car_id])))
