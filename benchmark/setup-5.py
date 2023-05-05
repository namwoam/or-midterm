# This setup is total random distrubution
from base import BaseBenchmark
import car_level
import car_rate
import start_site
import station
import orders

# must use car_rate->car_level->station->start_site->orders

benchmark = BaseBenchmark(10, 20, 5, 20, 5, 0)
car_rate.linear_car_rate(benchmark)
car_level.random_car_level(benchmark)
station.random_station(benchmark)
start_site.random_start_site(benchmark)
orders.random_orders(benchmark)

if __name__ == "__main__":
    print(benchmark)
