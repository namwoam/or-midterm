from MTP_lib import *
import os


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
    psudo_profit = 0
    spent_rearrage_time = 0
    step_limit = solution.n_S
    start_time = datetime(2023, 1, 1)
    candidate_count = solution.n_S
    step = 0
    while step <= step_limit:
        candidate_operation: list[Operation] = []
        for half_hour in solution.n_D*24*2:
            current_time = start_time + timedelta(minutes=half_hour*30)

    assignment, rearrangement = solution.output()
    return assignment, rearrangement


class Operation():
    def __init__(self, profit: int) -> None:
        self.profit = profit


class AcceptOrder(Operation):
    def __init__(self, profit: int, order: Order, car_id: int, time_cost: int) -> None:
        super().__init__(profit)
        self.order = order
        self.has_rearrangement = False
        self.time_cost = time_cost

    def attach_rearrangement(self, rearrangement: Rearragement):
        self.has_rearrangement = True
        self.rearrangement = rearrangement
        self.profit -= self.time_cost*(rearrangement.duration.seconds//60)


class DropOrder(Operation):
    def __init__(self, dropped_order: AcceptOrder, time_cost: int) -> None:
        if dropped_order.has_rearrangement == False:
            super().__init__(-1*dropped_order.profit)
        else:
            super().__init__(-1*dropped_order.profit+(dropped_order.time_cost + time_cost)
                             * (dropped_order.rearrangement.duration.seconds//60))
        self.dropped_order = dropped_order
