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

    # read data and store the information into your self-defined variables
    fp = open(os.path.join(os.path.dirname(__file__), file_path), 'r')

    lines = fp.readlines()
    Number_of_station, Number_of_car, number_of_level, number_of_order, number_of_day, moving_limit = map(
        int, lines[1].split(","))
    pointer = 4

    station_status = []  # 每個站點儲存不同level的車子數
    car_rent_status = {}  # 每個站點儲存的車子
    global car_level_fee
    car_level_fee = {}  # 每個車子的價位

    order = []  # 每個站點存不同的訂單排程
    distance = []  # 每個站之間的時間

    assignment_plan = []
    arrangement_plan = []

    for i in range(Number_of_station):
        station_status.append([0]*number_of_level)
        car_rent_status[i+1] = ([])
        distance.append([])

# 讓每個站點儲存不同level的車子數
    for i in range(Number_of_car):
        item = list(map(int, lines[pointer].strip().split(",")))
        car_rent_status[item[2]].append(item)
        station_status[item[2]-1][item[1]-1] += 1
        pointer += 1

    pointer += 2

# 每個level車子的價位
    for i in range(number_of_level):
        typ = list(map(int, lines[pointer].strip().split(",")))
        car_level_fee[typ[0]] = typ[1]
        pointer += 1

    pointer += 2

    for i in range(number_of_order):
        typ1 = lines[pointer].strip().split(",")[-2:]
        typ = list(map(int, lines[pointer].strip().split(",")[:-2]))+typ1
        pointer += 1
        order.append(typ)
        assignment_plan.append(0)
        arrangement_plan.append([])

    pointer += 2
    for i in range(Number_of_station):
        for j in range(Number_of_station):
            typ = list(map(int, lines[pointer].strip().split(",")))
            pointer += 1
            distance[i].append(typ[2])

# print(order)


# for a_row in fp:
#    print(a_row) # a_row is a list
# ...


# start your algorithm here
    assignment = []
    rearrangement = []
# ...

    return assignment, rearrangement
