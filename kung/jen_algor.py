from MTP_lib import *
from heapq import heapify, heappush, heappop


def heuristic_algorithm(file_path):
    '''
    1. Write your heuristic algorithm here.
    2. We will call this function from grading_program.py to evaluate your algorithm.
    3. Do not change the function name and the file name.
    4. Do not import any extra library. Note that we use the latest version of Pandas (v2.0.0, released on April 3, 2023), and there are several updates which might affect your program implementation.
    5. The parameter is the file path of a data file, whose format is specified in the midterm project document.
    6. You need to return your plan in two lists "assignment" and "rearrangement".
        (a) "assignment" is a one-dimensional integer list with size n_K. 
            (i)   If you plan to satisfy order i, store the ID of the car (an integer) that will be used to satisfy order i in assignment[i - 1]. 
            (ii)  If you plan to reject order i, store -1 (an integer representing negative one) in assignment[i - 1].
        (b) "rearrangement" is a two-dimensional list with size ncm * 4, where ncm denotes the number of car moving (may be different in different plans). For the kth moving: 
            (i)   Store the car ID (an integer) in rearrangement[k - 1][0]. 
            (ii)  Store the starting station ID (an integer) in rearrangement[k - 1][1]. 
            (iii) Store the ending station ID (an integer) in rearrangement[k - 1][2]. 
            (iv)  Store the rearragement starting time as a string in the "YYYY/MM/DD hh:mm" format in rearrangement[k - 1][3].
    7. The only PY file that you need and are allowed to submit is this algorithm_module.py.
    '''

    class Car():
        # runningCars = []
        def __init__(self, car_id: int, car_level: int, initial_station: int, available: int, rearrangeable: int) -> None:
            self.car_id = car_id
            self.car_level = car_level
            self.station = initial_station
            self.available = available
            self.rearrangeable = rearrangeable

        def accept_car(self, order):
            self.rearrangeable = order.return_time + 4
            self.available = order.return_time + 4.5
            self.station = order.return_station

    class Order():
        def __init__(self, order_id: int, level: int, pickup_station: int, return_station: int, pickup_time: float, return_time: float) -> None:
            self.order_id = order_id
            self.level = level
            self.pickup_station = pickup_station
            self.return_station = return_station
            self.pickup_time = pickup_time
            self.return_time = return_time

        '''
        def accept_or_not(self, order):
            print(upper_T)
            for i in range(self.cnt, n_K, 1):
                if(orders[i].pickup_time <= order.return_time):
                    self.cnt += 1
                    for j in range(int(2 * orders[i].pickup_time), int(2 * orders[i].return_time), 1):
                        self.half_hour_demands[j].orders.append(orders[i])
                else:
                    break
            for i in range(int(2 * order.pickup_time), int(2 * order.return_time), 1):
                if self.half_hour_demands[i].get_num_demand() > n_C:
                    result = sorted(self.half_hour_demands[i].orders, key = lambda x: (x.level, x.pickup_time), reverse = True)
                    if order.level <= result[n_K - 1]:
                        s
                    if order not in result[0: n_K]:
                       self.remove_order(order)
                       return False
            return True
        '''

    def read_file(file_path) -> None:
        nonlocal start_time
        nonlocal n_S, n_C, n_L, n_K, n_D, B
        nonlocal cars
        nonlocal orders
        nonlocal rates
        nonlocal distances
        with open(os.path.join(os.path.dirname(__file__), file_path), "r") as reader:
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
                    n_S, n_C, n_L, n_K, n_D, B = list(
                        map(int, line.split(",")))
                elif section == 1:
                    if line == "Car ID,Level,Initial station\n":
                        cars = [[] for i in range(n_L)]
                        continue
                    row = list(map(int, line.split(",")))
                    cars[row[1] - 1].append(Car(*row, 0, 0))
                elif section == 2:
                    if line == "Car level,Hour rate\n":
                        rates = [0 for i in range(n_L)]
                        continue
                    row = list(map(int, line.split(",")))
                    rates[row[0] - 1] = row[1]
                elif section == 3:
                    if line == "Order ID,Level,Pick-up station,Return station,Pick-up time,Return time\n":
                        continue
                    order_id, level, p_station, r_station, p_time, r_time = line.replace("\n", "").split(
                        ",")
                    order_id = int(order_id)
                    level = int(level)
                    p_station = int(p_station)
                    r_station = int(r_station)
                    p_time = (datetime.strptime(
                        p_time, '%Y/%m/%d %H:%M') - start_time).total_seconds() / 3600
                    r_time = (datetime.strptime(
                        r_time, '%Y/%m/%d %H:%M') - start_time).total_seconds() / 3600

                    orders.append(
                        Order(order_id, level, p_station, r_station, p_time, r_time))
                elif section == 4:
                    if line == "From,To,Distance\n":
                        distances = [[] for i in range(n_S)]
                        continue
                    f_station, t_station, station_distance = list(
                        map(int, line.split(",")))
                    distances[f_station -
                              1].append([station_distance, t_station])
        orders.sort(key=lambda x: x.pickup_time)
        for i in distances:
            i.sort(key=lambda x: x[0])

    '''
    class Demands():
        class HalfHourDemand():
            def __init__(self) -> None:
                self.orders = [] 
            def get_num_demand(self):
                return len(self.orders)
        nonlocal n_K
        nonlocal orders
        nonlocal n_C
        nonlocal t
        nonlocal upper_T
    

        def __init__(self) -> None:
            self.half_hour_demands = [self.HalfHourDemand() for i in range(2 * upper_T)]
            self.cnt = 0
        def remove_order(self, order):
            for i in range(2 * order.pickup_time, 2 * order.return_time, 0.5):
                self.half_hour_deamnds.orders.remove(order)
    '''

    def accept_order(order, car, level):
        # nonlocal useds
        nonlocal accepted
        nonlocal assignment
        nonlocal rearrangement
        nonlocal rates
        nonlocal profit

        car.accept_car(order)
        # useds.append((order, car))
        accepted = True
        assignment[order.order_id - 1] = int(car.car_id)
        profit += rates[level - 1] * (order.return_time - order.pickup_time)

    def rearrange_cars(d, car, order):
        # nonlocal useds
        # useds = [i for i in useds if d[1] != car]
        rearrangement.append([int(car.car_id), int(car.station), int(
            order.pickup_station), (start_time + timedelta(car.rearrangeable)).strftime("%Y/%m/%d %H:%M")])

    n_S = 0
    n_C = 0
    n_L = 0
    n_K = 0
    n_D = 0
    B = 0
    orders = []
    cars = []
    rates = []
    distances = []
    start_time = datetime(2023, 1, 1)

    read_file(file_path)
    # start your algorithm here
    assignment = [-1 for i in range(n_K)]
    rearrangement = []
    profit = 0
    re_hour = 0
    # useds = []  # (order, car) as element
    # demands  = Demands()
    # rearrangeCars = []
    t = 0
    cnt = 0
    # iterrate times for every 0.5 hour

    while cnt < n_K:
        while cnt < n_K and orders[cnt].pickup_time == t:
            order = orders[cnt]
            cnt += 1
            # whether to accept
            accepted = False
            for c in cars[order.level - 1]:
                if c.available <= t and c.station == order.pickup_station:
                    accept_order(order, c, order.level)
                    break
            # upgrade car lrvel
            if not accepted and order.level < n_L:
                for c in cars[order.level]:
                    if c.available <= t and c.station == order.pickup_station:
                        accept_order(order, c, order.level + 1)
                        break
            # rearrangement
            if not accepted:
                for i in distances[order.pickup_station - 1]:
                    if i[0] + re_hour <= B:
                        for j in filter(lambda x: x.station == i[1] and x.rearrangeable + i[0] / 60 + 0.5 <= t, cars[order.level-1]):
                            rearrange_cars(i, j, order)
                            accept_order(order, j, order.level)
                            accepted = True
                            break
                        if (not accepted and order.level < n_L):
                            for j in filter(lambda x: x.station == i[1] and x.rearrangeable + i[0] / 60 + 0.5 <= t, cars[order.level]):
                                rearrange_cars(i, j, order)
                                accept_order(order, j, order.level)
                                accepted = True
                                break
                    if accepted:
                        re_hour += i[0]
                        break
            if not accepted:
                profit -= 2 * rates[order.level - 1] * \
                    (order.return_time - order.pickup_time)
        t += 0.5
    print(file_path, 'profit =', profit)

    assignment = [int(i) for i in assignment]
    return assignment, rearrangement
