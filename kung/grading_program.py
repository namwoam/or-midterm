'''
You do not need to change the code in this file.
You only need to ensure that the TAs can run your algorithm here.
'''
from MTP_lib import *
from simulated_annealing import heuristic_algorithm as sa
from jen_algor import heuristic_algorithm as jen
from chen_sing_Yu_huristic import heuristic_algorithm as ch
from Jen_gurobi import heuristic_algorithm as op
from simpleHuristic import heuristic_algorithm as sim

import sys


def check_format(assignment, rearrangement):
    for i in assignment:
        if not isinstance(i, int):
            return False

    for rearrange in rearrangement:
        if not isinstance(rearrange[0], int) and not isinstance(rearrange[1], int) and not isinstance(rearrange[2], int):
            return False

        date_format = "%Y/%m/%d %H:%M"

        try:
            dateObject = datetime.strptime(rearrange[3], date_format)
        except ValueError:
            return False

        import re
        r = re.compile('.{4}/.{2}/.{2} .{2}:.{2}')
        if r.match(rearrange[3]) is None:
            return False

    return True


if __name__ == '__main__':
    folder_name = "testdata"
    # read all instances (.txt file) under data folder
    all_data_list = os.listdir(os.path.join(
        os.path.dirname(__file__), folder_name))

    # evaluate all instances
    result_df = pd.DataFrame(
        columns=['Data name', 'Time', 'Profit', 'Feasibility'])

    for file_name in all_data_list:
        print(f"start: {file_name}")
        start_time = t.time()
        profit = np.nan
        feasibility = False
        try:
            '''
                1. We will import your algorithm here and give you file_path (e.g.,'data/instance01.txt') as the function argument.
                2. You need to return two lists "assignment" and "rearrangement".
                '''
            file_path = f'{folder_name}/' + file_name
            assignment, rearrangement = sim(file_path)

        except BaseException as e:
            raise e
            print("the algorithm has errors")

        end_time = t.time()
        spent_time = end_time - start_time

        '''
        We will check the format, feasibility, and calculate the objective values here.
        '''
        if not check_format(assignment, rearrangement):
            print("the format has errors")

        print(f"validate: {file_name}")
        feasibility, profit = find_obj_value(
            file_path, assignment, rearrangement)

        result_df = pd.concat([result_df, pd.DataFrame([{'Data name': file_name,
                                                         'Time': spent_time,
                                                         'Profit': profit,
                                                         'Feasibility': feasibility}])], ignore_index=True)

# output result
result_df.to_csv('result.csv', index=False)
