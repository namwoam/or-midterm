from MTP_lib import *


def heuristic_algorithm(file_path):

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

    n_S = int(dfs[0].loc[0, "n_S"])  # 站點的數量
    n_C = int(dfs[0].loc[0, "n_C"])  # 車子的數量
    n_L = int(dfs[0].loc[0, "n_L"])  # 等級的數量
    n_K = int(dfs[0].loc[0, "n_K"])  # 訂單的數量
    n_D = int(dfs[0].loc[0, "n_D"])  # 總天數
    upper_T = n_D * 24
    B = int(dfs[0].loc[0, "B"])  # 最高移車上限
    move = B  # 總移出時數

    tmpCars = [Car(row['Car ID'], row['Level'], row['Initial station'], True, 0)
               for i, row in dfs[1].astype(int).iterrows()]
    car_station = [[] for _ in range(n_S)]  # 把桐站的車子放在同個index的list裡面

    for car in tmpCars:
        car_station[car.station-1].append(car)

    dash_board = [[0]*n_L for i in range(n_S)]  # 記錄站點i,level j 的車子目前有幾輛

    # 一個純數字的儀錶板，初始化目前各站有各levle的車數
    for i in tmpCars:
        dash_board[i.station-1][i.car_level - 1] += 1

    # 記錄不同等級車子的價格
    df_carPrice = dfs[2].astype(int)
    car_level_fee = df_carPrice.set_index('Car level')['Hour rate'].to_dict()

    df_orders = dfs[3]
    print(df_orders)
    df_orders.iloc[:, :4] = df_orders.iloc[:, :4].astype(int)
    df_orders.iloc[:, 4:6] = df_orders.iloc[:, 4:6].apply(pd.to_datetime)
    df_orders = df_orders.sort_values(by='Pick-up time', ascending=True)

    # 建立好所有訂單
    orders = [Order(row['Order ID'], row['Level'], row['Pick-up station'], row['Return station'],
                    row['Pick-up time'], row['Return time']) for i, row in df_orders.iterrows()]

    distances = [[] for i in range(n_S)]
    for i, row in dfs[4].astype(int).iterrows():
        # 從第i站出發到(距離,j站)
        distances[row['From'] - 1].append((row['Distance'], row['To']))
    for i in range(len(distances)):
        distances[i].sort(key=lambda x: x[0])
    print(distances)

    # 檢查兩個時段有沒有重疊
    def check_overlap(order1, order2, alpha=4.5):

        detal = 0
        if (order1.pickup_time < order2.pickup_time):
            detal = order2.pickup_time - order1.return_time
        else:
            detal = order1.pickup_time - order2.return_time
        hours_diff = detal.total_seconds() / 3600

        return hours_diff < 4.5

    # 檢查order2是不是在order1之後而且沒有重疊
    def check_totally_after(order1, order2):
        return order1.return_time + timedelta(hours=4.5) <= order2.pickup_time

    # 看看這個站有沒有符合顧客需要同級的車
    def check_samecar_avalibility(dash_board, order):
        if (dash_board[order.pickup_station-1][order.level-1] >= 1):
            return True
        return False

    # 看看這個站有沒有符合顧客升級的車
    def check_upgrade_avalibility(dash_board, order):
        # 要確保不會升到超過最大的階級
        if (order.level+1 <= n_L and dash_board[order.pickup_station-1][order.level] >= 1):
            return True
        return False

    def calculate_start_time(start_time, move_minute):
        real_start_time = start_time - timedelta(minutes=int(move_minute))
        return real_start_time.strftime('%Y/%m/%d %H:%M')

    # 計算選擇升級或移車決策的損失函數(car_level傳該車的價格，miss_order紀錄所有選這個決策而失去的訂單)

    def loss_caculator(car_level_fee, miss_order):
        loss = 0
        for item in miss_order:
            time_diff = item.return_time - item.pickup_time
            hours_diff = time_diff.total_seconds() / 3600
            loss = 2*car_level_fee*hours_diff
        return loss

    def count_objective_value(assignment, car_level_fee, order):
        objective = 0
        for i in range(len(order)):
            time_diff = orders[i].return_time - orders[i].pickup_time
            hours_diff = time_diff.total_seconds() / 3600
            reveune = car_level_fee[order[i].level]*hours_diff
            if (assignment[i] == -1):
                objective -= 2*reveune
            else:
                objective += reveune
        return objective

    # 這個決策變數會決定要"同級","升級","轉單",(從哪裡轉,車子的等級)"放單"(-1)
    def make_decision(renting_order, this_order, left_order, dash_board, car_level_fee, move, distances):

        # 放棄這單的成本
        give_up_cost = loss_caculator(
            car_level_fee[this_order.level], [this_order])
        same_cost = 0
        upgrade_cost = 0

        count_same = dash_board[this_order.pickup_station -
                                1][this_order.level-1]-1
        count_upgrade = 0

        miss_same = []
        miss_upgrade = []

        print("***decision_process***", '\n')
        print("前面已經接過的單", renting_order, '\n')

        # 如果是用same_car
        if (count_same != -1):

            for left in left_order:  # 檢查所有剩下的單，如果overlap就必須要檢查
                if (left != this_order and check_overlap(this_order, left)):
                    if (this_order.pickup_station == left.pickup_station and left.level == this_order.level):
                        count_same -= 1  # 如果同站同車，我就把這單扣掉
                    # 補車
                    for previous in renting_order:  # 如果之前結束的單，其return station等於left的intial station，且時間完全在他之後
                        if (this_order.pickup_station == previous.return_station and previous.level == this_order.level and check_totally_after(previous, left)):
                            count_same += 1
                    if count_same < 0:
                        miss_same.append(left)
                # 如果沒有重疊了，那就結束檢查
                elif (check_totally_after(this_order, left)):
                    same_cost = loss_caculator(
                        car_level_fee[this_order.level], miss_same)
                    break
        else:  # 如果不行用同樣的車
            same_cost = give_up_cost

        # 如果是用升級的車
        if (check_upgrade_avalibility(dash_board, this_order)):
            count_upgrade = dash_board[this_order.pickup_station -
                                       1][this_order.level]-1

            for left in left_order:  # 檢查所有剩下的單，如果overlap就必須要檢查
                if (left != this_order and check_overlap(this_order, left)):
                    if (this_order.pickup_station == left.pickup_station and left.level == this_order.level+1):
                        count_upgrade -= 1  # 如果同站同車，我就把這單扣掉
                    # 補車
                    for previous in renting_order:  # 如果之前結束的單，其return station等於left的intial station，且時間完全在他之後
                        if (this_order.pickup_station == previous.return_station and previous.level == this_order.level+1 and check_totally_after(previous, left)):
                            count_upgrade += 1
                    if count_upgrade < 0:
                        miss_upgrade.append(left)
                # 如果沒有重疊了，那就結束檢查，並計算總損失
                elif (check_totally_after(this_order, left)):
                    upgrade_cost = loss_caculator(
                        car_level_fee[this_order.level+1], miss_upgrade)
                    break
        else:  # 如果不行用同樣的車
            upgrade_cost = give_up_cost

        # 如果可以不移就不移，決定同車的話會回傳0,升級回傳1
        if (min(give_up_cost, same_cost, upgrade_cost) < give_up_cost):
            return (1, this_order.pickup_station, this_order.level) if same_cost < upgrade_cost else (2, this_order.pickup_station, this_order.level+1)

        return (-1, 0, 0)  # 真的不行的話回傳-1

    # 下訂單後進行操作

    take_order = []
    renting_car = []

    assignment = [0]*n_K  # fix住k單的建造計畫
    rearrangement = []  # 紀錄那些要移動

    for i in range(0, n_K):

        # 先補車
        while (len(take_order) != 0):
            if check_totally_after(take_order[0], orders[i]):
                dash_board[take_order[0].return_station -
                           1][renting_car[0].car_level-1] += 1
                car_station[take_order[0].return_station -
                            1].append(renting_car[0])
                renting_car.remove(renting_car[0])
                take_order.remove(take_order[0])
            else:
                break

       # decesion[0]是要做什麼決策[1]是使用的車站(如果是move則是從哪裡搬來)[2]需要的車子的levle
        decision = make_decision(
            take_order, orders[i], orders[i:], dash_board, car_level_fee, move, distances)
        print(i, decision)

        # 如果決定放棄這單
        if (decision[0] == -1):
            assignment[i] = -1
            continue

       # 如果是選擇同站同車
        elif (decision[0] == 1):
            take_order.append(orders[i])  # 決定選這單
            dash_board[orders[i].pickup_station -
                       1][orders[i].level-1] -= 1  # 這類車在這個站點的數量扣1
           # 取車，找同站目前有等級一樣的車
            for car in car_station[decision[1]-1]:
                if (car.car_level == decision[2]):
                    renting_car.append(car)  # 把它加到目前租借
                    assignment[i] = car.car_id
                    car_station[decision[1]-1].remove(car)  # 把現在車子去掉
                    break

        # 如果是選同站升級的車
        elif (decision[0] == 2):
            take_order.append(orders[i])  # 決定選這單
            dash_board[orders[i].pickup_station -
                       1][orders[i].level] -= 1  # 這類車在這個站點的數量扣1
            for car in car_station[decision[1]-1]:  # 取車，找同站目前有等級一樣的車
                if (car.car_level == decision[2]):
                    renting_car.append(car)  # 把它加到目前租借
                    assignment[i] = car.car_id
                    car_station[decision[1]-1].remove(car)
                    break

            rearrangement.append(detail)

    print(move)

    objective_value = count_objective_value(assignment, car_level_fee, orders)
    print("objective_value", objective_value)
    print(assignment)
    print(rearrangement)

    return assignment, rearrangement
