from MTP_lib import *
from heapq import heapify, heappush, heappop


class Car():
    def __init__(self, car_id: int, car_level: int, initial_station: int, available: bool, rearrangeable: int) -> None:
        self.car_id = car_id
        self.car_level = car_level
        self.station = initial_station
        self.available = available
        self.rearrangeable = rearrangeable


class Order():
    def __init__(self, order_id: int, level: int, pickup_station: int, return_station: int, pickup_time: float, return_time: float) -> None:
        self.order_id = order_id
        self.level = level
        self.pickup_station = pickup_station
        self.return_station = return_station
        self.pickup_time = pickup_time
        self.return_time = return_time


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

    # read data and store the information into your self-defined variables
    dfs = []
    fp = open(os.path.join(os.path.dirname(__file__), file_path), 'r')
    start = True
    for a_row in fp:
        # print(a_row) # a_row is a list
        a_row = a_row.replace('\n', '')
        if a_row == "==========":
            start = True
            continue
        row = a_row.split(",")
        if start:
            dfs.append(pd.DataFrame(columns=row))
            start = False
        else:
            n = len(dfs)-1
            dfs[n].loc[len(dfs[n])] = row

    n_S = int(dfs[0].loc[0, "n_S"])
    n_C = int(dfs[0].loc[0, "n_C"])
    n_L = int(dfs[0].loc[0, "n_L"])
    n_K = int(dfs[0].loc[0, "n_K"])
    n_D = int(dfs[0].loc[0, "n_D"])
    upper_T = n_D * 24
    B = int(dfs[0].loc[0, "B"])

    tmpCars = [Car(row['Car ID'], row['Level'], row['Initial station'], True, 0)
               for i, row in dfs[1].astype(int).iterrows()]
    cars = [[] for i in range(n_L)]
    # classify cars by level
    for i in tmpCars:
        cars[i.car_level - 1].append(i)
    df_carPrice = dfs[2].astype(int)
    start_time = datetime(2023, 1, 1)
    df_orders = dfs[3]
    df_orders.iloc[:, :4] = df_orders.iloc[:, :4].astype(int)
    df_orders.iloc[:, 4:6] = df_orders.iloc[:, 4:6].apply(pd.to_datetime).apply(
        lambda x: (x - start_time).dt.total_seconds() / 3600)
    df_orders = df_orders.sort_values(by='Pick-up time', ascending=True)
    orders = [Order(row['Order ID'], row['Level'], row['Pick-up station'], row['Return station'],
                    row['Pick-up time'], row['Return time']) for i, row in df_orders.iterrows()]
    distances = [[] for i in range(n_S)]
    for i, row in dfs[4].astype(int).iterrows():
        distances[row['From'] - 1].append((row['Distance'], row['To']))
    for i in range(len(distances)):
        distances[i].sort(key=lambda x: x[0])

    # start your algorithm here
    assignment = [-1 for i in range(n_K)]
    rearrangement = []
    profit = 0
    re_hour = 0
    useds = []  # (order, car) as element
    # rearrangeCars = []
    t = 0
    cnt = 0
    # iterrate times for every 0.5 hour

    def accept_order(order, car, level):
        nonlocal useds
        nonlocal accepted
        nonlocal assignment
        nonlocal rearrangement
        nonlocal df_carPrice
        nonlocal profit
        nonlocal upper_T

        car.available = False
        car.rearrangeable = order.return_time + 4
        car.station = order.return_station
        useds.append((order, car))
        accepted = True
        assignment[order.order_id - 1] = int(car.car_id)
        profit += df_carPrice.loc[level - 1, 'Hour rate'] * \
            (order.return_time - order.pickup_time)

    def rearrange_cars(d, car, order):
        nonlocal useds
        useds = [i for i in useds if d[1] != car]
        rearrangement.append([int(car.car_id), int(car.station), int(order.pickup_station), (
            start_time + timedelta(hours=car.rearrangeable)).strftime("%Y/%m/%d %H:%M")])

    while cnt < n_K:
        for i in useds:
            (order, car) = i
            if (order.return_time + 4.5) == t:
                car.available = True
                useds.remove((order, car))

        while cnt < n_K and orders[cnt].pickup_time == t:
            order = orders[cnt]
            cnt += 1
            # whether to accept
            accepted = False
            for c in cars[order.level - 1]:
                if c.available == True and c.station == order.pickup_station:
                    accept_order(order, c, order.level)
                    break
            # upgrade car lrvel
            if not accepted and order.level < n_L:
                for c in cars[order.level]:
                    if c.available == True and c.station == order.pickup_station:
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
                            for j in filter(lambda x: x.station == i[1] and x.rearrangeable + i[1] / 60 + 0.5 <= t, cars[order.level]):
                                rearrange_cars(i, j, order)
                                accept_order(order, j, order.level)
                                accepted = True
                                break
                    if accepted:
                        re_hour += i[0]
                        break
            if not accepted:
                profit -= 2 * \
                    df_carPrice.loc[order.level - 1, 'Hour rate'] * \
                    (order.return_time - order.pickup_time)
        t += 0.5
    print(file_path, 'profit =', profit)

    assignment = [int(i) for i in assignment]
    return assignment, rearrangement
