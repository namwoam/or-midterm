import datetime


class Car():
    def __init__(self, car_id: int, car_level: int, initial_station: int = -1) -> None:
        self.car_id = car_id
        self.car_level = car_level
        self.initial_station = initial_station

    def __str__(self) -> str:
        assert self.initial_station != -1, "No initial station"
        return f"{self.car_id},{self.car_level},{self.initial_station}"


class Rates():
    def __init__(self, car_level: int, hour_rate: int) -> None:
        self.car_level = car_level
        self.hour_rate = hour_rate

    def __str__(self) -> str:
        return f"{self.car_level},{self.hour_rate}"


class Order():
    def __init__(self, order_id: int,  level: int, pickup_station: int, return_station: int, pickup_time: datetime.datetime, return_time: datetime.datetime) -> None:
        self.order_id = order_id
        self.level = level
        self.pickup_station = pickup_station
        self.return_station = return_station
        self.pickup_time = pickup_time
        self.return_time = return_time

    def __str__(self) -> str:
        return f"{self.order_id},{self.level},{self.pickup_station},{self.return_station},{self.pickup_time.strftime('%Y/%m/%d %H:%M')},{self.return_time.strftime('%Y/%m/%d %H:%M')}"


class Distances():
    def __init__(self, station_count: int) -> None:
        self.station_count = station_count
        self.stations = [(0, 0) for _ in range(self.station_count)]

    def __str__(self) -> str:
        result = []
        for from_station in range(self.station_count):
            for to_station in range(self.station_count):
                result.append(
                    f"{from_station+1},{to_station+1},{abs(self.stations[from_station][0]-self.stations[to_station][0])+abs(self.stations[from_station][1]-self.stations[to_station][1])}")
        return "\n".join(result)


class BaseBenchmark():
    def __init__(self, n_S: int, n_C: int, n_L: int, n_K: int, n_D: int, B: int) -> None:
        self.n_S = n_S
        self.n_C = n_C
        self.n_L = n_L
        self.n_K = n_K
        self.n_D = n_D
        self.b = B
        self.cars: list[Car] = []
        self.rates: list[Rates] = []
        self.orders: list[Order] = []
        self.distance: Distances = Distances(self.n_S)

    def __str__(self) -> str:
        lines = []
        lines.append("n_S,n_C,n_L,n_K,n_D,B")
        lines.append(
            f"{self.n_S},{self.n_C},{self.n_L},{self.n_K},{self.n_D},{self.b}")
        lines.append("==========")
        lines.append("Car ID,Level,Initial station")
        lines.extend([str(car) for car in self.cars])
        lines.append("==========")
        lines.append("Car level,Hour rate")
        lines.extend([str(rate) for rate in self.rates])
        lines.append("==========")
        lines.append(
            "Order ID,Level,Pick-up station,Return station,Pick-up time,Return time")
        lines.extend([str(order) for order in self.orders])
        lines.append("==========")
        lines.append("From,To,Distance")
        lines.append(str(self.distance))
        lines.append("==========")

        return "\n".join(lines)
