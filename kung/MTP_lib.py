import time as t
import itertools
import math
import os
import pandas as pd  # version: 2.0.0
import numpy as np
from gurobipy import *
import datetime


class Solution:
    def __init__(self, file_path) -> None:
        self.cars: list[Car] = []
        self.rates: list[Rates] = []
        self.orders: list[Order] = []
        self.distance: list[list[int]] = []
        self.assignment: list[int] = []
        self.rearragement: list[Rearragement] = []
        with open(file_path, "r") as reader:
            section = 0
            for line in reader.readlines():
                if len(line) == 0:
                    continue
                if line == "==========\n":
                    section += 1
                    continue
                if section == 0:
                    if line == "n_S,n_C,n_L,n_K,n_D,B\n":
                        continue
                    self.n_S, self.n_C, self.n_L, self.n_K,  self.n_D, self.B = list(
                        map(int, line.split(",")))
                elif section == 1:
                    if line == "Car ID,Level,Initial station\n":
                        continue
                    self.cars.append(Car(*list(map(int, line.split(",")))))
                elif section == 2:
                    if line == "Car level,Hour rate\n":
                        continue
                    self.rates.append(Rates(*list(map(int, line.split(",")))))
                elif section == 3:
                    if line == "Order ID,Level,Pick-up station,Return station,Pick-up time,Return time\n":
                        continue
                    order_id, level, p_station, r_station, p_time, r_time = line.replace("\n", "").split(
                        ",")
                    order_id = int(order_id)
                    level = int(level)
                    p_station = int(p_station)
                    r_station = int(r_station)
                    p_time = datetime.datetime.strptime(
                        p_time, '%Y/%m/%d %H:%M')
                    r_time = datetime.datetime.strptime(
                        r_time, '%Y/%m/%d %H:%M')

                    self.orders.append(
                        Order(order_id, level, p_station, r_station, p_time, r_time))
                elif section == 4:
                    if line == "From,To,Distance\n":
                        continue
                    f_station, t_station, station_distance = list(
                        map(int, line.split(",")))
                    print(f_station, t_station, station_distance)
                    if f_station != len(self.distance):
                        self.distance.append([station_distance])
                    else:
                        self.distance[-1].append(station_distance)

    def output(self):
        return self.assignment, [[rearragement.car_id, rearragement.starting_station, rearragement.end_staion, rearragement.start_time.strftime('%Y/%m/%d %H:%M')] for rearragement in self.rearragement]


class Car():
    def __init__(self, car_id: int, car_level: int, initial_station: int = -1) -> None:
        self.car_id = car_id
        self.car_level = car_level
        self.initial_station = initial_station


class Rates():
    def __init__(self, car_level: int, hour_rate: int) -> None:
        self.car_level = car_level
        self.hour_rate = hour_rate


class Order():
    def __init__(self, order_id: int,  level: int, pickup_station: int, return_station: int, pickup_time: datetime.datetime, return_time: datetime.datetime) -> None:
        self.order_id = order_id
        self.level = level
        self.pickup_station = pickup_station
        self.return_station = return_station
        self.pickup_time = pickup_time
        self.return_time = return_time
        self.accept = False


class Rearragement():
    def __init__(self, car_id: int, starting_station: int, ending_station: int, start_time: datetime) -> None:
        self.car_id = car_id
        self.starting_station = starting_station
        self.end_staion = ending_station
        self.start_time = start_time
        pass
