from operator import attrgetter
from MTP_lib import *
import os
import math


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
    solution = Solution(os.path.join(os.path.dirname(__file__), file_path))
    print(f"start on:{file_path}")
    psudo_profit = 0
    spent_rearrage_time = 0
    step_limit = solution.n_K
    candidate_count = 100
    past_operation: list[Operation] = []
    step = 0
    real_step = 0
    while step <= step_limit and real_step <= 2*step_limit:
        print(f"iteration:{step}, psudo_profit={psudo_profit}")
        candidate_operation: list[Operation] = []
        solution.update_history()
        for order in choices(solution.orders, k=solution.n_K // solution.n_S):
            if order.accept == False:
                profit = 3 * (order.return_time - order.pickup_time).total_seconds()//(
                    60*60) * solution.rates[order.level-1].hour_rate
                for car in solution.cars:
                    if solution.try_accept_new_order(order.order_id, car.car_id) == True:
                        candidate_operation.append(
                            AcceptOrder(profit, order, car.car_id))
                        break
        real_step += 1
        if len(candidate_operation) == 0:
            continue
        step += 1
        real_step = step
        conduct_operation = max(candidate_operation, key=attrgetter('profit'))
        assert isinstance(conduct_operation, Operation)
        past_operation.append(conduct_operation)
        psudo_profit += conduct_operation.profit
        if isinstance(conduct_operation, AcceptOrder):
            solution.orders[conduct_operation.order.order_id -
                            1].accept = True
            solution.orders[conduct_operation.order.order_id -
                            1].accept_car_id = conduct_operation.car_id
    df = pd.DataFrame(solution.car_history)
    assignment, rearrangement = solution.output()
    print(assignment)
    return assignment, rearrangement


class Operation():
    def __init__(self, profit: int) -> None:
        self.profit = profit


class AcceptOrder(Operation):
    def __init__(self, profit: int, order: Order, car_id: int, time_cost: int = 0) -> None:
        super().__init__(profit)
        self.order = order
        self.has_rearrangement = False
        self.time_cost = time_cost
        self.car_id = car_id

    def attach_rearrangement(self, rearrangement: Rearragement):
        assert self.time_cost != 0
        self.has_rearrangement = True
        self.rearrangement = rearrangement
        self.profit -= self.time_cost * \
            int((rearrangement.duration.total_seconds())//60)


class DropOrder(Operation):
    def __init__(self, dropped_order: AcceptOrder, time_cost: int) -> None:
        if dropped_order.has_rearrangement == False:
            super().__init__(-1*dropped_order.profit)
        else:
            super().__init__(-1*dropped_order.profit+(dropped_order.time_cost + time_cost)
                             * (dropped_order.rearrangement.duration.total_seconds()//60))
        self.dropped_order = dropped_order
