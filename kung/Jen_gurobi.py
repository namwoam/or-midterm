from MTP_lib import *


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
        def __init__(self, car_id: int, car_level: int, initial_station: int) -> None:
            self.car_id = car_id
            self.car_level = car_level
            self.station = initial_station

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

    # read file
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
                B /= 60
            elif section == 1:
                if line == "Car ID,Level,Initial station\n":
                    continue
                row = list(map(int, line.split(",")))
                cars.append(Car(*row))
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
                distances[f_station - 1].append([station_distance, t_station])
    for i in distances:
        i.sort(key=lambda x: x[1])
    distances = [[j[0] for j in i] for i in distances]

    V = 30 * 24 * 2
    N = range(1, n_K + 1, 1)
    N_0 = range(0, n_K + 1, 1)
    M = range(0, n_C, 1)
    I = range(0, n_S, 1)
    C_0 = 4  # delay + cleaning time
    C_1 = 0.5  # preperation time
    start_time = datetime(2023, 1, 1)
    L_c = [i.car_level for i in cars]
    L_o = [j.level for j in orders]
    S = [i.pickup_time for i in orders]
    R = [i.return_time for i in orders]
    P = [rates[i.level - 1] for i in orders]
    D = [[0 for k in N_0] for j in N_0]
    A = [[0 for j in N_0] for i in M]
    A_1 = [[0 for j in N_0] for i in M]

    for j in N_0:
        for k in N_0:
            if (j != 0 and k != 0):
                D[j][k] = distances[orders[j - 1].return_station -
                                    1][orders[k - 1].pickup_station - 1] / 60
    for i in M:
        for j in N_0:
            if (j != 0):
                A[i][j] = distances[cars[i].station -
                                    1][orders[j - 1].pickup_station - 1] / 60
                if (A[i][j] > 0):
                    A_1[i][j] = 1
    print("Model init")
    model = Model("MTP")
    model.Params.LogToConsole = 0
    print("vars init")
    x = model.addVars(M, N_0, N_0, lb=0, vtype=GRB.BINARY, name='x')
    a = model.addVars(M, N, lb=0, vtype=GRB.BINARY, name='a')

    # objective function
    model.setObjective(quicksum(a[i, j] * P[j - 1] * (R[j-1] - S[j-1]) for i in M for j in N) - 2 * quicksum(
        (1 - quicksum(a[i, j] for i in M)) * P[j - 1] * (R[j-1] - S[j-1]) for j in N), GRB.MAXIMIZE)
    print("constr init")
    # constraints
    constr = model.addConstrs(
        quicksum(x[i, j, k] for i in M for j in N_0 if j != k) <= 1 for k in N)
    constr = model.addConstrs(
        quicksum(x[i, j, k] for i in M for k in N_0 if j != k) <= 1 for j in N)
    constr = model.addConstrs(quicksum(x[i, j, k] for j in N_0 if j != k) == quicksum(
        x[i, k, h] for h in N_0 if h != k) for i in M for k in N)
    constr = model.addConstrs((R[k-1] - R[j-1]) + V * (1 - x[i, j, k]) >= C_0 + D[j][k] + (
        R[k-1] - S[k-1]) + C_1 for i in M for j in N for k in N if j != k)
    constr = model.addConstrs(R[k-1] + V * (1 - x[i, 0, k]) >= A[i][k] + (
        R[k-1] - S[k-1]) + C_1 * A_1[i][k] for i in M for k in N if j != k)
    constr = model.addConstrs(quicksum(x[i, 0, j] for j in N) <= 1 for i in M)
    constr = model.addConstr(quicksum(D[j][k] * x[i, j, k] for i in M for j in N for k in N if j !=
                             k) + quicksum(A[i][k] * x[i, 0, k] for i in M for k in N) <= B)
    constr = model.addConstrs(
        quicksum(x[i, j, k] for k in N_0 if j != k) == a[i, j] for i in M for j in N)
    constr = model.addConstrs(
        (L_c[i] - L_o[j-1]) * a[i, j] <= 1 for i in M for j in N)
    constr = model.addConstrs(
        (L_c[i] - L_o[j-1]) * a[i, j] >= 0 for i in M for j in N)
    print("constrs done")
    model.optimize()
    print("optimize done")

    assignment = [-1 for i in orders]
    for j in N:
        for i in M:
            if a[i, j].x == 1:
                assignment[j - 1] = i + 1

    rearrangement = []
    for i in M:
        for j in N_0:
            for k in N:
                if x[i, j, k].x == 1:
                    if j == 0:
                        if cars[i].station != orders[k-1].pickup_station:
                            rearrangement.append([i+1, int(cars[i].station), int(
                                orders[k-1].pickup_station), start_time.strftime("%Y/%m/%d %H:%M")])
                    elif orders[j-1].return_station != orders[k-1].pickup_station:
                        rearrangement.append([i+1, int(orders[j-1].return_station), int(orders[k-1].pickup_station),
                                             (start_time + timedelta(hours=orders[j-1].return_time + 4)).strftime("%Y/%m/%d %H:%M")])

    print(file_path, 'profit =', model.getObjective().getValue())
    return assignment, rearrangement
