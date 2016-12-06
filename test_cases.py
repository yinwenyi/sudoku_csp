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
    
def binary_model_import(stu_models, gac):
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

def check_GAC2(stu_models, stu_orderings, stu_prop):
    score = 0
    try:
        board = easyBoards[0]
        start = time.time()
        csp, var_array = stu_models.sudoku_csp_model_gac(board)
        end = time.time()
        runtime = end - start
        print(runtime)

        solver = BT(csp)
        # solver.trace_on()
        start = time.time()
        #solver.bt_search(stu_prop.FC_BT, stu_orderings.ord_random, stu_orderings.val_arbitrary)
        solver.bt_search(stu_prop.FC_BT, stu_orderings.ord_custom, stu_orderings.val_lcv)
        end = time.time()
        runtime = end - start
        print(runtime)

        details = ""

    except Exception:
        details = "One or more runtime errors occurred while importing board into model 1: %r" % traceback.format_exc()

    return score, details

def check_GAC(stu_models, stu_orderings, stu_prop):
    score = 0
    try:
        board = easyBoards[0]
        start = time.time()
        csp, var_array = stu_models.sudoku_csp_model_gac(board)
        end = time.time()
        runtime = end - start
        print(runtime)

        solver = BT(csp)
        # solver.trace_on()
        start = time.time()
        solver.bt_search(stu_prop.FC_BT, stu_orderings.ord_random, stu_orderings.val_arbitrary)
        #solver.bt_search(stu_prop.FC_BT, stu_orderings.ord_custom, stu_orderings.val_lcv)
        end = time.time()
        runtime = end - start
        print(runtime)

        details = ""

    except Exception:
        details = "One or more runtime errors occurred while importing board into model 1: %r" % traceback.format_exc()

    return score, details
    
def check_ForwaringChecking(stu_models, stu_orderings, stu_prop):
    score = 0
    try:
        board = easyBoards[0]
        csp, var_array = stu_models.sudoku_csp_model_binary(board)
            
        solver = BT(csp)
        # solver.trace_on()
        solver.bt_search(stu_prop.FC_BT, stu_orderings.ord_random, stu_orderings.val_arbitrary)

        if check_solution(var_array):
            score = 5
            details = ""
        else:
            details = "Solution found in full run with LCV heuristic on %s was not a valid solution." % name
        
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

    import orderings as stu_orderings
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
    
    print("---starting binary_model_import without GAC enforce---")
    score,details = binary_model_import(stu_models, False)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished binary_model_import without GAC enforce---\n")

    print("---starting check_GAC2 custom---")
    score,details = check_GAC2(stu_models, stu_orderings, stu_prop)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished check_GAC2 custom---\n")

    print("---starting check_GAC---")
    score,details = check_GAC(stu_models, stu_orderings, stu_prop)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished check_GAC---\n")

    # print("---starting check_ForwaringChecking---")
    # score,details = check_ForwaringChecking(stu_models, stu_orderings, stu_prop)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished check_ForwaringChecking---\n")
    #
    # print("---starting check_model_1_constraints_enum_rewscols---")
    # score,details = check_model_1_constraints_enum_rewscols(stu_models)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished check_model_1_constraints_enum_rewscols---\n")
    #
    # print("---starting check_model_2_constraints_enum_rewscols---")
    # score,details = check_model_2_constraints_enum_rewscols(stu_models)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished check_model_2_constraints_enum_rewscols---\n")
    #
    # print("---starting binary model 1---")
    # score,details = check_binary_constraint_model_1(stu_models)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished binary model 1---\n")
    #
    # print("---starting nary model 2---")
    # score,details = check_nary_constraint_model_2(stu_models)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished nary model 2---\n")
    #
    # print("---starting unsolvable model 1---")
    # score,details = test_UNSAT_problem_model_1(stu_models, stu_orderings)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished unsolvable model 1---\n")
    #
    # print("---starting unsolvable model 2---")
    # score,details = test_UNSAT_problem_model_2(stu_models, stu_orderings)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished unsolvable model 2---\n")
    #
    # print("---starting sat tuples model 1---")
    # score, details = test_sat_tuples(stu_models.hitori_csp_model_1, stu_orderings)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished sat tuples model 1---\n")
    #
    # print("---starting sat tuples model 2---")
    # score, details = test_sat_tuples(stu_models.hitori_csp_model_2, stu_orderings)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished sat tuples model 2---\n")
    #
    # print("---starting small problem model 1---")
    # score, details = test_small_case(stu_models.hitori_csp_model_1, stu_orderings)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished small problem model 1---\n")
    #
    # print("---starting small problem model 2---")
    # score, details = test_small_case(stu_models.hitori_csp_model_2, stu_orderings)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished small problem model 2---\n")
    # print("---STARTING ORDERING TESTS---\n")
    #
    # print("---starting test_ord_dh---")
    # score, details = test_ord_dh(stu_models.hitori_csp_model_2, stu_orderings)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished test_ord_dh---\n")
    #
    # print("---starting test_ord_mrv---")
    # score, details = test_ord_mrv(stu_models.hitori_csp_model_2, stu_orderings)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished test_ord_mrv---\n")
    #
    # print("---STARTING FULL RUN TESTS---\n")
    #
    # print("---starting test_big_problem---\n")
    # score, details = test_big_problem(stu_models.hitori_csp_model_1, stu_orderings)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished test_big_problem---\n")
    #
    # print("---starting full run model 1---")
    # score, details = test_full_run(stu_models.hitori_csp_model_1, stu_orderings)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished full model 1---\n")
    #
    # print("---starting full run model 2---")
    # score, details = test_full_run(stu_models.hitori_csp_model_2, stu_orderings)
    # print(details)
    # print("score: %d" % score)
    # total_score += score
    # print("---finished full run model 2---\n")
    #
    # if total_score == TOTAL_POINTS:
    #     print("Score: %d/%d; Passed all tests" % (total_score,TOTAL_POINTS))
    # else:
    #     print("Score: %d/%d; Did not pass all tests." % (total_score,TOTAL_POINTS))

if __name__=="__main__":
    main()
