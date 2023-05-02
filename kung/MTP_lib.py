import time as t
import itertools
import math
import os
import pandas as pd  # version: 2.0.0
import numpy as np
from gurobipy import *
from datetime import *
from random import *


class Solution:
    def __init__(self, file_path) -> None:
        self.cars: list[Car] = []
        self.rates: list[Rates] = []
        self.orders: list[Order] = []
        self.distance: list[list[int]] = []
        self.assignment: list[int] = []
        self.rearragement: list[Rearragement] = []
        self.begin_time = datetime(2023, 1, 1)
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
                    p_time = datetime.strptime(
                        p_time, '%Y/%m/%d %H:%M')
                    r_time = datetime.strptime(
                        r_time, '%Y/%m/%d %H:%M')

                    self.orders.append(
                        Order(order_id, level, p_station, r_station, p_time, r_time))
                elif section == 4:
                    if line == "From,To,Distance\n":
                        continue
                    f_station, t_station, station_distance = list(
                        map(int, line.split(",")))
                    if f_station != len(self.distance):
                        self.distance.append([station_distance])
                    else:
                        self.distance[-1].append(station_distance)
        self.car_history = np.zeros((self.n_C, self.n_D*24*2))

    def output(self):
        self.assignment = [-1 for _ in range(len(self.orders))]
        for i, order in enumerate(self.orders):
            self.assignment[i] = order.accept_car_id
        return self.assignment, [[rearragement.car_id, rearragement.starting_station, rearragement.end_staion, rearragement.start_time.strftime('%Y/%m/%d %H:%M')] for rearragement in self.rearragement]

    def update_from_outside(self):
        for i, assignment in enumerate(self.assignment):
            self.orders[i].accept_car_id = assignment
            if assignment == -1:
                self.orders[i].accept = False
            else:
                self.orders[i].accept = True

    def get_profit(self):
        self.update_from_outside()
        profit = 0
        for order in self.orders:
            time_duration = order.return_time - order.pickup_time
            hour_duration = (time_duration.total_seconds()) // (60*60)
            if order.accept == True:
                profit += self.rates[order.level -
                                     1].hour_rate * hour_duration
            else:
                profit -= 2 * self.rates[order.level -
                                         1].hour_rate * hour_duration
        return profit

    def init_history(self):
        self.car_history = np.zeros((self.n_C, self.n_D*24*2))
        for i,  car in enumerate(self.cars):
            self.car_history[i] = car.initial_station

    def update_history(self):
        self.init_history()
        for order in self.orders:
            if order.accept == True:
                start_time = order.pickup_time
                end_time = order.return_time+timedelta(hours=4.5)
                self.make_car_unavailable(
                    order.accept_car_id, start_time, end_time, order.pickup_station,  order.return_station)
        for rearrangement in self.rearragement:
            start_time = rearrangement.start_time
            end_time = rearrangement.start_time + \
                rearrangement.duration + timedelta(hours=0.5)
            self.make_car_unavailable(rearrangement.car_id, start_time, end_time,
                                      rearrangement.starting_station, rearrangement.end_staion)

    def try_accept_new_order(self, order_id: int, car_id: int):
        order = self.orders[order_id-1]
        car = self.cars[car_id-1]
        start_time = order.pickup_time
        end_time = order.return_time+timedelta(hours=4.5)
        if not (order.level == car.car_level or order.level+1 == car.car_level):
            return False
        try:
            self.make_car_unavailable(
                car_id, start_time, end_time, order.pickup_station, order.pickup_station, True)
            return True
        except AssertionError:
            return False

    def make_car_unavailable(self, car_id: int, start_time: datetime, end_time: datetime, from_station: int, return_station: int, trying: bool = False):
        start_half_hour = int(
            (start_time - self.begin_time).total_seconds())//(60*30)
        end_half_hour = math.ceil(
            int((end_time - self.begin_time).total_seconds())/(60*30))
        assert np.all(self.car_history[car_id -
                                       1][start_half_hour:end_half_hour+1] == from_station)
        if trying:
            return
        self.car_history[car_id-1, start_half_hour:end_half_hour] = -1
        self.car_history[end_half_hour:] = return_station

    def get_feasibility(self, debug=False):
        self.update_from_outside()
        start_time = datetime(2023, 1, 1)
        stations: list[list[int]] = []
        total_used_rearrange_time = 0  # in minutes
        for order in self.orders:
            print(order)
        for _ in range(self.n_S):
            stations.append([])
        for car in self.cars:
            stations[car.initial_station-1].append(car.car_id)
        for half_hour in range(self.n_D*24*2):
            current_time = start_time + timedelta(minutes=30*half_hour)
            if debug:
                print(f"At: {current_time.isoformat()}")
            if total_used_rearrange_time > self.B:
                if debug:
                    print("Total time exceed B")
                return False
            for rearrange in self.rearragement:
                if rearrange.start_time == current_time:
                    if rearrange.car_id in stations[rearrange.starting_station-1]:
                        stations[rearrange.starting_station -
                                 1].remove(rearrange.car_id)
                        if debug:
                            print(
                                f"Rearrange: car {rearrange.car_id} leave from station {rearrange.starting_station} on {rearrange.start_time}")
                    else:
                        print(
                            f"car {rearrange.car_id} not exist at station {rearrange.starting_station} at rearrange ")
                        return False
                if rearrange.start_time + rearrange.duration >= current_time and rearrange.start_time + rearrange.duration < current_time + timedelta(minutes=30):
                    total_used_rearrange_time += self.distance[rearrange.starting_station -
                                                               1][rearrange.end_staion-1]
                    stations[rearrange.end_staion-1].append(rearrange.car_id)
                    if debug:
                        print(
                            f"Rearrange: car {rearrange.car_id} return to station {rearrange.end_staion}")
            for order in self.orders:
                if order.accept == True and order.pickup_time == current_time:
                    if order.accept_car_id in stations[order.pickup_station-1]:
                        stations[order.pickup_station -
                                 1].remove(order.accept_car_id)
                        if debug:
                            print(
                                f"Order {order.order_id}:car {order.accept_car_id} leave from station {order.pickup_station}")
                    else:

                        print(
                            f"Order {order.order_id}:car {order.accept_car_id} not exist at station {order.pickup_station} at assignment")
                        return False
                if order.accept == True and order.return_time == current_time:
                    stations[order.return_station -
                             1].append(order.accept_car_id)
                    if debug:
                        print(
                            f"Order {order.order_id}:car {order.accept_car_id} return to station {order.return_station}")

        return True


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
    def __init__(self, order_id: int,  level: int, pickup_station: int, return_station: int, pickup_time: datetime, return_time: datetime) -> None:
        self.order_id = order_id
        self.level = level
        self.pickup_station = pickup_station
        self.return_station = return_station
        self.pickup_time = pickup_time
        self.return_time = return_time
        self.accept = False
        self.accept_car_id = -1

    def __str__(self) -> str:
        return f"Order {self.order_id}, accepeted by car:{self.accept_car_id}, at station {self.pickup_station} in {self.pickup_time.isoformat()}"


class Rearragement():
    def __init__(self, car_id: int, starting_station: int, ending_station: int, start_time: datetime, duration: timedelta) -> None:
        self.car_id = car_id
        self.starting_station = starting_station
        self.end_staion = ending_station
        self.start_time = start_time
        self.duration = duration


def find_obj_value(file_path: str, assignment: list[int], rearrangement: list[list[any]]):
    solution = Solution(os.path.join(os.path.dirname(__file__), file_path))
    solution.assignment = assignment
    solution.rearragement = []
    print(rearrangement)
    for list_rearrangement in rearrangement:
        car_id, starting_station, end_station, start_time = list_rearrangement
        car_id = int(car_id)
        starting_station = int(starting_station)
        ending_station = int(end_station)
        start_time = datetime.strptime(start_time, '%Y/%m/%d %H:%M')
        solution.rearragement.append(Rearragement(
            car_id, starting_station, ending_station, start_time, timedelta(minutes=solution.distance[starting_station-1][end_station-1])))
    return solution.get_feasibility(), solution.get_profit()
