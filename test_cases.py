import sys
from cspbase import *
from propagators import *
import itertools
import traceback
import pickle
import time

##############
##MODEL TEST CASES

# Get the easy test cases
f = open('testcases/easy1011_parsed.pkl', 'rb')
easyBoards = pickle.load(f)

##Checking that variables are initialized with correct domains in model 1.
##Passing this test is a prereq for passing check_model_1_constraints.
def model_1_import(stu_models):
    score = 0
    try:
        board = easyBoards[0]
        csp, var_array = stu_models.sudoku_csp_model(board)
        answer = []
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    answer.append(9)
                else:
                    answer.append(1)

        lister = []
        for i in range(9):
            for j in range(9):
                lister.append(len(var_array[i][j].cur_domain()))

        if lister != answer:
            #details = "FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister)
            details = "Failed to import a board into model 1: initial domains don't match"
        else:
            details = ""
            score = 1
    except Exception:
        details = "One or more runtime errors occurred while importing board into model 1: %r" % traceback.format_exc()

    return score,details

##Checking that variables are initialized with correct domains in model 2.
##Passing this test is a prereq for passing check_model_2_constraints.
def model_2_import(stu_models):
    score = 1
    details = ""
    try:
        board = easyBoards[0]
        csp, var_array = stu_models.sudoku_csp_model_gac(board)
        answer = [[7, 9, 4, 5, 8, 2, 1, 3, 6], [2, 6, 8, 9, 3, 1, 7, 4, 5], [3, 1, 5, 4, 7, 6, 9, 8, 2], [6, 8, 9, 7, 1, 5, 3, 2, 4], [4, 3, 2, 8, 6, 9, 5, 7, 1], [1, 5, 7, 2, 4, 3, 8, 6, 9], [8, 2, 1, 6, 5, 7, 4, 9, 3], [9, 4, 3, 1, 2, 8, 6, 5, 7], [5, 7, 6, 3, 9, 4, 2, 1, 8]]
        for i in range(9):
            for j in range(9):
                if answer[i][j] not in var_array[i][j].cur_domain():
                    details = "No valid solution found"
                    score = 0
                    break
            if score == 0:
                break
    except Exception:
        details = "One or more runtime errors occurred while importing board into model 2: %r" % traceback.format_exc()

    return score,details
    
def binary_model_import(stu_models, gac, VarSelect, VarAssign):
    score = 0
    try:
        board = easyBoards[0]
        csp, var_array = stu_models.sudoku_csp_model_binary(board, gac)
        answer = []
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    answer.append(9)
                else:
                    answer.append(1)

        lister = []
        for i in range(9):
            for j in range(9):
                lister.append(len(var_array[i][j].cur_domain()))

        if lister != answer:
            #details = "FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister)
            details = "Failed to import a board into model 1: initial domains don't match"
        else:
            details = ""
            score = 1
    except Exception:
        details = "One or more runtime errors occurred while importing board into model 1: %r" % traceback.format_exc()

    return score,details

    
def all_diff_model_run(stu_models, Backtracking, VarSelect, VarAssign):
    score = 0
    try:
        for i in range(10):
          print("Testing board {}".format(i))
          board = easyBoards[i]
          start = time.time()
          csp, var_array = stu_models.sudoku_csp_model(board)
          end = time.time()
          runtime = end - start
          print("Time to encode CSP = {}".format(runtime))

          solver = BT(csp)
          # solver.trace_on()
          # start = time.time()
          solver.bt_search(Backtracking, VarSelect, VarAssign)
          # end = time.time()
          # runtime = end - start
          # print(runtime)

          details = ""

    except Exception:
        details = "One or more runtime errors occurred while importing board into model 1: %r" % traceback.format_exc()

    return score, details
    
def all_diff_GAC_model_run(stu_models, Backtracking, VarSelect, VarAssign):
    score = 0
    try:
        for i in range(10):
          print("Testing board {}".format(i))
          board = easyBoards[i]
          start = time.time()
          csp, var_array = stu_models.sudoku_csp_model_gac(board)
          end = time.time()
          runtime = end - start
          print("Time to encode CSP = {}".format(runtime))

          solver = BT(csp)
          # solver.trace_on()
          # start = time.time()
          solver.bt_search(Backtracking, VarSelect, VarAssign)
          # end = time.time()
          # runtime = end - start
          # print(runtime)

          details = ""

    except Exception:
        details = "One or more runtime errors occurred while importing board into model 1: %r" % traceback.format_exc()

    return score, details
    
def binary_model_run(stu_models, gac, Backtracking, VarSelect, VarAssign):
    score = 0
    try:
        for i in range(10):
          print("Testing board {}".format(i))
          board = easyBoards[i]
          start = time.time()
          csp, var_array = stu_models.sudoku_csp_model_binary(board, gac)
          end = time.time()
          runtime = end - start
          print("Time to encode CSP = {}".format(runtime))

          solver = BT(csp)
          # solver.trace_on()
          # start = time.time()
          solver.bt_search(Backtracking, VarSelect, VarAssign)
          # end = time.time()
          # runtime = end - start
          # print(runtime)

          details = ""

    except Exception:
        details = "One or more runtime errors occurred while importing board into model 1: %r" % traceback.format_exc()

    return score, details
    
def check_ForwaringChecking(stu_models, VarSelect, VarAssign):
    score = 0
    try:
        board = easyBoards[0]
        csp, var_array = stu_models.sudoku_csp_model_binary(board)
            
        solver = BT(csp)
        # solver.trace_on()
        solver.bt_search(stu_prop.FC_BT, stu_orderings.ord_random, stu_orderings.val_arbitrary)

        
    except Exception:
        details = "One or more runtime errors occurred while importing board into model 1: %r" % traceback.format_exc()

    return score,details

########################################
## Other helpers that may be of use
#Checks whether a solution given by BT is correct.
def check_solution(hitori_variable_array):
    for i in range(len(hitori_variable_array)):
        row_sol = []
        blacks = [False] * len(hitori_variable_array)
        for j in range(len(hitori_variable_array)):
            if hitori_variable_array[i][j].get_assigned_value() != 0:
                row_sol.append(hitori_variable_array[i][j].get_assigned_value())
                blacks[j] = False
            else:
                if blacks[j - 1] or blacks[j]:
                    print("1")
                    return False
                else:
                    blacks[j] = True
        if not check_list(row_sol):
            print("2")
            return False

    for i in range(len(hitori_variable_array)):
        row_sol = []
        blacks = [False] * len(hitori_variable_array)
        for j in range(len(hitori_variable_array)):
            if hitori_variable_array[j][i].get_assigned_value() != 0:
                row_sol.append(hitori_variable_array[j][i].get_assigned_value())
                blacks[j] = False
            else:
                if blacks[j - 1] or blacks[j]:
                    print("3")
                    return False
                else:
                    blacks[j] = True
        if not check_list(row_sol):
            print("4")
            return False

    return True

##Helper function that checks if a given list is valid
def check_list(solution_list):
    return len(solution_list) == len(set(solution_list))

##RUN TEST CASES
def main(stu_propagators=None, stu_models=None):
    TOTAL_POINTS = 37
    total_score = 0

    import orderings_bill as stu_orderings
    import hitori_csp as stu_models
    import propagators as stu_prop

    print("---STARTING MODEL TESTS---\n")

    # print("---starting model_1_import---")
    # score,details = model_1_import(stu_models)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished model_1_import---\n")

    # print("---starting model_gac_import---")
    # score,details = model_2_import(stu_models)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished model_gac_import---\n")
    
    print("---starting binary_model_run without GAC enforce---")
    print("Running plain backtracking with random var selection and random var assignment")
    score,details = binary_model_run(stu_models, False, stu_prop.prop_BT, stu_orderings.ord_random, stu_orderings.val_arbitrary)
    print(details)
    print("Running plain backtracking with MRV and LCV")
    score,details = binary_model_run(stu_models, False, stu_prop.prop_BT, stu_orderings.ord_mrv, stu_orderings.val_lcv)
    print(details)
    print("Running plain backtracking with DH and LCV")
    score,details = binary_model_run(stu_models, False, stu_prop.prop_BT, stu_orderings.ord_dh, stu_orderings.val_lcv)
    print(details)
    print("Running FC backtracking with random var selection and random var assignment")
    score,details = binary_model_run(stu_models, False, stu_prop.FC_BT, stu_orderings.ord_random, stu_orderings.val_arbitrary)
    print(details)
    print("Running FC backtracking with MRV and LCV")
    score,details = binary_model_run(stu_models, False, stu_prop.FC_BT, stu_orderings.ord_mrv, stu_orderings.val_lcv)
    print(details)
    print("Running FC backtracking with DH and LCV")
    score,details = binary_model_run(stu_models, False, stu_prop.FC_BT, stu_orderings.ord_dh, stu_orderings.val_lcv)
    print(details)
    print("---finished binary_model_run without GAC enforce---\n")
    
    print("---starting binary_model_run with GAC enforce---")
    print("Running plain backtracking with random var selection and random var assignment")
    score,details = binary_model_run(stu_models, True, stu_prop.prop_BT, stu_orderings.ord_random, stu_orderings.val_arbitrary)
    print(details)
    print("Running plain backtracking with MRV and LCV")
    score,details = binary_model_run(stu_models, True, stu_prop.prop_BT, stu_orderings.ord_mrv, stu_orderings.val_lcv)
    print(details)
    print("Running plain backtracking with DH and LCV")
    score,details = binary_model_run(stu_models, True, stu_prop.prop_BT, stu_orderings.ord_dh, stu_orderings.val_lcv)
    print(details)
    print("Running FC backtracking with random var selection and random var assignment")
    score,details = binary_model_run(stu_models, True, stu_prop.FC_BT, stu_orderings.ord_random, stu_orderings.val_arbitrary)
    print(details)
    print("Running FC backtracking with MRV and LCV")
    score,details = binary_model_run(stu_models, True, stu_prop.FC_BT, stu_orderings.ord_mrv, stu_orderings.val_lcv)
    print(details)
    print("Running FC backtracking with DH and LCV")
    score,details = binary_model_run(stu_models, True, stu_prop.FC_BT, stu_orderings.ord_dh, stu_orderings.val_lcv)
    print(details)
    print("---finished binary_model_run with GAC enforce---\n")

    print("---starting all_diff_model_run without GAC enforce---")
    print("Running plain backtracking with random var selection and random var assignment")
    score,details = all_diff_model_run(stu_models, stu_prop.prop_BT, stu_orderings.ord_random, stu_orderings.val_arbitrary)
    print(details)
    print("Running plain backtracking with MRV and LCV")
    score,details = all_diff_model_run(stu_models, stu_prop.prop_BT, stu_orderings.ord_mrv, stu_orderings.val_lcv)
    print(details)
    print("Running plain backtracking with DH and LCV")
    score,details = all_diff_model_run(stu_models, stu_prop.prop_BT, stu_orderings.ord_dh, stu_orderings.val_lcv)
    print(details)
    print("Running FC backtracking with random var selection and random var assignment")
    score,details = all_diff_model_run(stu_models, stu_prop.FC_BT, stu_orderings.ord_random, stu_orderings.val_arbitrary)
    print(details)
    print("Running FC backtracking with MRV and LCV")
    score,details = all_diff_model_run(stu_models, stu_prop.FC_BT, stu_orderings.ord_mrv, stu_orderings.val_lcv)
    print(details)
    print("Running FC backtracking with DH and LCV")
    score,details = all_diff_model_run(stu_models, stu_prop.FC_BT, stu_orderings.ord_dh, stu_orderings.val_lcv)
    print(details)
    print("---finished all_diff_model_run without GAC enforce---\n")

    print("---starting all_diff_GAC_model_run with GAC enforce---")
    print("Running plain backtracking with random var selection and random var assignment")
    score,details = all_diff_GAC_model_run(stu_models, stu_prop.prop_BT, stu_orderings.ord_random, stu_orderings.val_arbitrary)
    print(details)
    print("Running plain backtracking with MRV and LCV")
    score,details = all_diff_GAC_model_run(stu_models, stu_prop.prop_BT, stu_orderings.ord_mrv, stu_orderings.val_lcv)
    print(details)
    print("Running plain backtracking with DH and LCV")
    score,details = all_diff_GAC_model_run(stu_models, stu_prop.prop_BT, stu_orderings.ord_dh, stu_orderings.val_lcv)
    print(details)
    print("Running FC backtracking with random var selection and random var assignment")
    score,details = all_diff_GAC_model_run(stu_models, stu_prop.FC_BT, stu_orderings.ord_random, stu_orderings.val_arbitrary)
    print(details)
    print("Running FC backtracking with MRV and LCV")
    score,details = all_diff_GAC_model_run(stu_models, stu_prop.FC_BT, stu_orderings.ord_mrv, stu_orderings.val_lcv)
    print(details)
    print("Running FC backtracking with DH and LCV")
    score,details = all_diff_GAC_model_run(stu_models, stu_prop.FC_BT, stu_orderings.ord_dh, stu_orderings.val_lcv)
    print(details)
    print("---finished all_diff_GAC_model_run with GAC enforce---\n")

if __name__=="__main__":
    main()
