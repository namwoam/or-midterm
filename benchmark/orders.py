from base import BaseBenchmark, Order
from random import randint, choice
from datetime import datetime, timedelta
from config import START_TIME


def random_orders(benchmark: BaseBenchmark):
    order_count = benchmark.n_K
    start_time = START_TIME
    end_time = START_TIME + timedelta(days=benchmark.n_D)
    total_time_delta = end_time - start_time
    total_time_delta_halfhour = (total_time_delta.total_seconds()//60)//30
    level_count = len(benchmark.rates)
    station_count = benchmark.distance.station_count
    for order_id in range(1, order_count+1):
        pickup_time_halfhour = randint(0, total_time_delta_halfhour)
        pickup_time = start_time + timedelta(minutes=30*pickup_time_halfhour)
        duration_hour = randint(
            0, (total_time_delta_halfhour - pickup_time_halfhour)//2)
        return_time = pickup_time + timedelta(minutes=duration_hour*60)
        order = Order(order_id, randint(1, level_count), randint(
            1, station_count), randint(1, station_count), pickup_time, return_time)
        benchmark.orders.append(order)
