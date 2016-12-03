import sys
from cspbase import *
from propagators import *
import itertools
import traceback

##############
##MODEL TEST CASES (HITORI)

##Checking that variables are initialized with correct domains in model 1.
##Passing this test is a prereq for passing check_model_1_constraints.
def model_1_import(stu_models):
    score = 0
    try:
        board = [[1, 3, 4, 1], [3, 1, 2, 4],[2, 4, 2, 3], [1, 2, 3, 2]]
        answer = [[0, 1], [0, 3], [0, 4], [0, 1], [0, 3], [0, 1], [0, 2], [0, 4], [0, 2], [0, 4], [0, 2], [0, 3], [0, 1], [0, 2], [0, 3], [0, 2]]

        csp, var_array = stu_models.hitori_csp_model_1(board)
        lister = []

        for i in range(4):
            for j in range(4):
                lister.append(var_array[i][j].cur_domain())

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
    score = 0
    try:
        board = [[1, 3, 4, 1], [3, 1, 2, 4],[2, 4, 2, 3], [1, 2, 3, 2]]
        answer = [[0, 1], [0, 3], [0, 4], [0, 1], [0, 3], [0, 1], [0, 2], [0, 4], [0, 2], [0, 4], [0, 2], [0, 3], [0, 1], [0, 2], [0, 3], [0, 2]]

        csp, var_array = stu_models.hitori_csp_model_2(board)
        lister = []

        for i in range(4):
            for j in range(4):
                lister.append(var_array[i][j].cur_domain())

        if lister != answer:
            #details = "FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister)
            details = "Failed to import a board into model 2: initial domains don't match"
        else:
            details = ""
            score = 1
    except Exception:
        details = "One or more runtime errors occurred while importing board into model 2: %r" % traceback.format_exc()

    return score,details


##Checks that model 1 constraints pass when all numbers different in each row and column, and fail when not all different.
def check_model_1_constraints_enum_rewscols(stu_models):
    score = 1
    details = []
    try:
        # do not use inequalities here
        # must be converted to hitori board
        board = [[3, 2, 1],[1, 3, 2],[3, 1, 2]]

        csp, var_array = stu_models.hitori_csp_model_1(board)

        for cons in csp.get_all_cons():
            all_vars = cons.get_scope()
            taken = []
            domain_list = []
            should_pass = []
            should_fail = []
            for va in all_vars:
                domain_list.append(va.cur_domain())
                if len(va.cur_domain()) == 1:
                    taken.append(va.cur_domain()[0])
            for i in range(len(all_vars)):
                va = all_vars[i]
                domain = domain_list[i]
                if len(domain) == 1:
                    should_pass.append(domain[0])
                    should_fail.append(domain[0])
                else:
                    for i in range(1,4):
                        if i in domain and i in taken:
                            should_fail.append(i)
                            break
                    for i in range(1,4):
                        if i in domain and i not in taken:
                            should_pass.append(i)
                            taken.append(i)
                            break
                    ##SWITCHING SHOULD PASS AND SHOULD FAIL HERE TO TEST
                    #for i in range(1,4):
                    #    if i in domain and i in taken:
                    #        should_pass.append(i)
                    #        break
                    #for i in range(1,4):
                    #    if i in domain and i not in taken:
                    #        should_fail.append(i)
                    #        taken.append(i)
                    #        break
            if cons.check(should_fail) != cons.check(should_pass):
                if cons.check(should_fail) or not cons.check(should_pass):
                    if not cons.check(should_fail):
                        #details.append("FAILED\nConstraint %s should be falsified by %r" % (str(cons),should_fail))
                        #details.append("var domains:")
                        #for va in all_vars:
                        #    details.append(va.cur_domain())
                        details.append("Failed constraint test in model 1: %s should be falsified by %r" % (str(cons), should_fail))
                    if cons.check(should_pass):
                        #details.append("FAILED\nConstraint %s should be satisfied by %r" % (str(cons),should_pass))
                        #details.append("var domains:")
                        #for va in all_vars:
                        #    details.append(va.cur_domain())
                        details.append("Failed constraint test in model 1: %s should be satisfied by %r" % (str(cons), should_fail))
                    details = "\n".join(details)
                    return 0,details

    except Exception:
        details.append("One or more runtime errors occurred while testing constraints in model 1: %r" % traceback.format_exc())
        details = "\n".join(details)
        return 0,details

    details.append("")
    details = "\n".join(details)
    return score,details

##Checks that model 2 constraints pass when all numbers different in each row and column, and fail when not all different.
def check_model_2_constraints_enum_rewscols(stu_models):
    score = 1
    details = []
    try:

        board = [[3, 2, 1],[1, 3, 2],[3, 1, 2]]

        csp, var_array = stu_models.hitori_csp_model_2(board)

        for cons in csp.get_all_cons():
            all_vars = cons.get_scope()
            taken = []
            domain_list = []
            should_pass = []
            should_fail = []
            for va in all_vars:
                domain_list.append(va.cur_domain())
                if len(va.cur_domain()) == 1:
                    taken.append(va.cur_domain()[0])
            for i in range(len(all_vars)):
                va = all_vars[i]
                domain = domain_list[i]
                if len(domain) == 1:
                    should_pass.append(domain[0])
                    should_fail.append(domain[0])
                else:
                    for i in range(1,4):
                        if i in domain and i in taken:
                            should_fail.append(i)
                            break
                    for i in range(1,4):
                        if i in domain and i not in taken:
                            should_pass.append(i)
                            taken.append(i)
                            break
            if cons.check(should_fail) != cons.check(should_pass):
                if cons.check(should_fail) or not cons.check(should_pass):
                    if not cons.check(should_fail):
                        #details.append("FAILED\nConstraint %s should be falsified by %r" % (str(cons),should_fail))
                        #details.append("var domains:")
                        #for va in all_vars:
                        #    details.append(va.cur_domain())
                        details.append("Failed constraint test in model 2: %s should be falsified by %r" % (str(cons), should_fail))
                    if cons.check(should_pass):
                        #details.append("FAILED\nConstraint %s should be satisfied by %r" % (str(cons),should_pass))
                        #details.append("var domains:")
                        #for va in all_vars:
                        #    details.append(va.cur_domain())
                        details.append("Failed constraint test in model 2: %s should be satisfied by %r" % (str(cons), should_fail))
                    details = "\n".join(details)
                    return 0,details

    except Exception:
        details.append("One or more runtime errors occurred while testing constraints in model 2: %r" % traceback.format_exc())
        details = "\n".join(details)
        return 0,details

    details.append("")
    details = "\n".join(details)
    return score,details

##Checks that students only have constraints over two variables for model 1.
def check_binary_constraint_model_1(stu_model):
    score = 2

    try:
        #must be converted to hitori board
        board = [[1, 3, 4, 1], [3, 1, 2, 4],[2, 4, 2, 3], [1, 2, 3, 2]]

        csp,var_array = stu_model.hitori_csp_model_1(board)

        all_cons = csp.get_all_cons()

        for con in all_cons:
            all_vars = con.get_scope()

            if len(all_vars) != 2:
                return 0, "Model 1 specifies ONLY binary constraints. Found a constraint of length %d" % len(all_vars)
        return score, ""

    except Exception:
        details = "One or more runtime errors occurred while testing model 1: %r" % traceback.format_exc()
    return 0, details

##Checks that students only have constraints over n variables in model 2.
def check_nary_constraint_model_2(stu_model):
    score = 2

    try:
        #must be converted to hitori board        
        board = [[1, 3, 4, 1], [3, 1, 2, 4],[2, 4, 2, 3], [1, 2, 3, 2]]

        csp,var_array = stu_model.hitori_csp_model_2(board)

        all_cons = csp.get_all_cons()

        saw_nary = False

        for con in all_cons:
            all_vars = con.get_scope()

            if len(all_vars) != 4:
                return 0, "Model 2 specifies ONLY n-ary constraints. Found a constraint of length %d" % len(all_vars)

            return score, ""

    except Exception:
        details = "One or more runtime errors occurred while testing model 2: %r" % traceback.format_exc()
    return 0, details

##Checks that BT fails to assign values to variables given students' constraints when problem is unsolvable in model 1.
def test_UNSAT_problem_model_1(stu_model, stu_orderings):
    score = 4
    try:
        board = [[3, 3, 3], [3, 3, 3], [3, 3, 3]]

        csp,var_array = stu_model.hitori_csp_model_1(board)

        solver = BT(csp)
        solver.bt_search(prop_BT, stu_orderings.ord_mrv, stu_orderings.val_arbitrary)

        for i in range(len(var_array)):
            for j in range(len(var_array)):
                if var_array[i][j].get_assigned_value() is not None:
                    #return 0,"FAILED\n cell [%d][%d] assigned %r; but problem is unsovable" % (i,j,var_array[i][j].get_assigned_value())
                    return 0,"Failed model 1 test: 'solved' unsolvable problem"

        return score, ""

    except Exception:

        details = "One or more runtime errors occurred while testing model 1 and an unsolvable problem: %r" % traceback.format_exc()
    return 0,details

##Checks that BT fails to assign values to variables given students' constraints when problem is unsolvable in model 1.

def test_UNSAT_problem_model_2(stu_model, stu_orderings):
    score = 4
    try:
        board = [[3, 3, 3], [3, 3, 3], [3, 3, 3]]

        csp,var_array = stu_model.hitori_csp_model_2(board)

        solver = BT(csp)
        solver.bt_search(prop_BT, stu_orderings.ord_mrv, stu_orderings.val_arbitrary)
        for i in range(len(var_array)):
            for j in range(len(var_array)):
                if var_array[i][j].get_assigned_value() is not None:
                    #return 0,"FAILED\n cell [%d][%d] assigned %r; but problem is unsovable" % (i,j,var_array[i][j].get_assigned_value())
                    return 0,"Failed model 2 test: 'solved' unsolvable problem"

        return score, ""

    except Exception:
        details = "One or more runtime errors occurred while testing model 2 and an unsolvable problem: %r" % traceback.format_exc()
    return 0,details

##Checks that small solution of a single grid is initialized correctly.
##In binary case there should be no constraints created, in n-ary case there should be 0 or 2 constraints (one for row, col).
def test_small_case(model, name=""):
    score = 2
    try:
        board = [[1]]
        answer = [0, 1]

        csp, var_array = model(board)
        if len(csp.get_all_cons()) != 0 and len(csp.get_all_cons()) != 2:
            return 0, "Failed small test: not the right number of constraints, have %d constraints" % len(csp.get_all_cons())
        if csp.get_all_vars()[0].domain() != answer:
            return 0, "Failed small test: domain of single variable is not correct."

        return 1, ""

    except Exception:
        details = "One or more runtime errors occurred while using %s on a large problem: %r" % (
            name, traceback.format_exc())

    return 0, details

##Checks that the satisfying tuples for each constraint are initialized correclty.

def test_sat_tuples(model, name=""):
    score = 1
    try:
        board = [[1, 2], [2, 1]]
        sat_tuples_1 = [[1, 2], [0, 2], [1, 0]]
        sat_tuples_2 = [[2, 1], [2, 0], [0, 1]]

        csp, var_array = model(board)
        i = 0
        for con in csp.get_all_cons():
            if len(con.sat_tuples) > 3:
                return 0, "Failed sat_tuples test, too many satisfying tuples."
            if con.get_scope()[0].domain() == [0, 1]:
               for tuple in sat_tuples_1:
                   if not con.check(tuple):
                       print(tuple)
                       return 0, "Failed sat_tuples test, missing a satisfying tuple."
            else:
                for tuple in sat_tuples_2:
                    if not con.check(tuple):
                        print(tuple)
                        return 0, "Failed sat_tuples test, missing a satisfying tuple."

        return score, ""

    except Exception:
        details = "One or more runtime errors occurred while using %s on a large problem: %r" % (
        name, traceback.format_exc())

    return 0, details

##Checks that students' code is able to encode constraints over a large problem
##BT may take a long time!
def test_big_problem(fn, stu_orderings, name=""):
    score = 5

    try:
        board = [[8 ,8, 1, 11, 8, 5, 3, 7, 8, 9, 12, 8],
                 [1, 8 ,8, 1, 9, 1, 12 ,6, 5, 2, 7 , 4],
                 [8, 5, 2, 7, 10, 4, 3, 9, 6, 10, 1, 12],
                 [8, 3, 1, 1, 9, 2, 6, 6, 7, 12, 7, 10],
                 [7, 3, 11, 8, 4, 5, 10, 5, 4, 3, 6, 4],
                 [10, 12, 2, 2, 2, 9, 10, 4, 1, 9, 11, 6],
                 [4, 8, 10, 10, 6, 1, 9, 5, 3, 7, 4, 8],
                 [11, 1, 7, 10, 9, 12, 1, 2, 5, 4, 3, 9],
                 [7, 10, 10, 12, 7, 3 , 2, 1, 9, 3, 4, 11],
                 [12, 9, 4, 12, 3, 5, 7, 5, 11, 1, 1, 5],
                 [5, 7, 11, 4, 3, 6, 5, 3, 9, 8, 10 ,2],
                 [10, 2, 5, 3, 1, 10, 4, 8, 12, 7, 9, 9]]

        csp, var_array = fn(board)
        solver = BT(csp)
        solver.bt_search(prop_BT, stu_orderings.ord_mrv, stu_orderings.val_arbitrary)

        if check_solution(var_array):
            return score, ""
        else:
            #return 0,"FAILED\nExplanation:\nvariable domains should be: %r\nvariable domains are: %r" % (answer,lister)
            return 0, "Failed on a large problem using %s" % name

    except Exception:
        details = "One or more runtime errors occurred while using %s on a large problem: %r" % (name, traceback.format_exc())

    return 0,details


##Checks that students' code is able to encode proper constraints over some problem.
def test_full_run(model, stu_orderings, name=""):
    score = 0
    try:
        board = [[2, 2, 2, 4, 2],
                [5, 1, 4, 2, 3],
                [5, 4, 2, 3, 5],
                [4 ,1, 1, 1, 2],
                [2, 3, 5, 1, 2]]


        csp,var_array = model(board)
        solver = BT(csp)
        solver.bt_search(prop_BT, stu_orderings.ord_mrv, stu_orderings.val_arbitrary)

        if check_solution(var_array):
            score = 5
            details = ""
        else:
            details = "Solution found in full run with MRV heuristic on %s was not a valid Hitori solution." % name

    except Exception:

        details = "One or more runtime errors occurred while trying a full run on %s: %r" % (name, traceback.format_exc())

    if score < 5:
        try:
            board = [[2, 2, 2, 4, 2],
                     [5, 1, 4, 2, 3],
                     [5, 4, 2, 3, 5],
                     [4, 1, 1, 1, 2],
                     [2, 3, 5, 1, 2]]


            csp,var_array = model(board)
            solver = BT(csp)
            solver.bt_search(prop_BT, stu_orderings.ord_dh, stu_orderings.val_arbitrary)

            if check_solution(var_array):
                score = 5
                details = ""
            else:
                details = "Solution found in full run with DH heuristic on %s was not a valid Hitori solution." % name
        except Exception:
            details = "One or more runtime errors occurred while trying a full run on %s: %r" % (name, traceback.format_exc())

    if score < 5:
        try:
            board = [[2, 2, 2, 4, 2],
                     [5, 1, 4, 2, 3],
                     [5, 4, 2, 3, 5],
                     [4, 1, 1, 1, 2],
                     [2, 3, 5, 1, 2]]

            csp,var_array = model(board)
            solver = BT(csp)
            solver.bt_search(prop_BT, stu_orderings.ord_random, stu_orderings.val_lcv)

            if check_solution(var_array):
                score = 5
                details = ""
            else:
                details = "Solution found in full run with LCV heuristic on %s was not a valid Hitori solution." % name
        except Exception:
            details = "One or more runtime errors occurred while trying a full run on %s: %r" % (name, traceback.format_exc())

    return score,details

def test_ord_dh(model, stu_orderings):

        score = 0
        details = ""

        board = [[2, 2, 2, 4, 2],
                [5, 1, 4, 2, 3],
                [5, 4, 2, 3, 5],
                [4, 1, 1, 1, 2],
                [2, 3, 5, 1, 2]]

        assigned = [[0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 0],
                    [1, 1, 1, 0, 0],
                    [1, 1, 0, 0, 0],
                    [1, 0, 0, 0, 0]]    


        try:
            csp,var_array = model(board)

            count = 0
            for i in range(0,len(board)):
                for j in range(0,len(board[0])):
                    if (assigned[i][j]):
                        csp.vars[count].assign(board[i][j])
                    count += 1

            var = stu_orderings.ord_dh(csp)

            if((var.name) == csp.vars[4].name):
                return 1, ""

            return 0, "Failed to locate the variable with the highest degree."

        except Exception:
            details = "One or more runtime errors occurred while trying to test ord_dh."

        return 0, details


def test_ord_mrv(model, stu_orderings):
    board = [[0,0,0],[0,0,0],[0,0,0]]
    score = 0
    details = ""

    try:
        csp,var_array = model(board)

        count = 0
        for i in range(0,len(board)):
            for j in range(0,len(board[0])):
                csp.vars[count].add_domain_values(range(0, count))
                count += 1

        var = stu_orderings.ord_mrv(csp)

        if((var.name) == csp.vars[0].name):
            return 1, ""

    except Exception:
        details = "One or more runtime errors occurred while trying to test ord_mrv"

    return 0, details


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

    print("---STARTING MODEL TESTS---\n")

    print("---starting model_1_import---")
    score,details = model_1_import(stu_models)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished model_1_import---\n")

    print("---starting model_2_import---")
    score,details = model_2_import(stu_models)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished model_2_import---\n")

    print("---starting check_model_1_constraints_enum_rewscols---")
    score,details = check_model_1_constraints_enum_rewscols(stu_models)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished check_model_1_constraints_enum_rewscols---\n")

    print("---starting check_model_2_constraints_enum_rewscols---")
    score,details = check_model_2_constraints_enum_rewscols(stu_models)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished check_model_2_constraints_enum_rewscols---\n")

    print("---starting binary model 1---")
    score,details = check_binary_constraint_model_1(stu_models)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished binary model 1---\n")

    print("---starting nary model 2---")
    score,details = check_nary_constraint_model_2(stu_models)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished nary model 2---\n")

    print("---starting unsolvable model 1---")
    score,details = test_UNSAT_problem_model_1(stu_models, stu_orderings)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished unsolvable model 1---\n")

    print("---starting unsolvable model 2---")
    score,details = test_UNSAT_problem_model_2(stu_models, stu_orderings)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished unsolvable model 2---\n")

    print("---starting sat tuples model 1---")
    score, details = test_sat_tuples(stu_models.hitori_csp_model_1, stu_orderings)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished sat tuples model 1---\n")

    print("---starting sat tuples model 2---")
    score, details = test_sat_tuples(stu_models.hitori_csp_model_2, stu_orderings)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished sat tuples model 2---\n")

    print("---starting small problem model 1---")
    score, details = test_small_case(stu_models.hitori_csp_model_1, stu_orderings)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished small problem model 1---\n")

    print("---starting small problem model 2---")
    score, details = test_small_case(stu_models.hitori_csp_model_2, stu_orderings)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished small problem model 2---\n")
    print("---STARTING ORDERING TESTS---\n")

    print("---starting test_ord_dh---")
    score, details = test_ord_dh(stu_models.hitori_csp_model_2, stu_orderings)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished test_ord_dh---\n")

    print("---starting test_ord_mrv---")
    score, details = test_ord_mrv(stu_models.hitori_csp_model_2, stu_orderings)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished test_ord_mrv---\n")

    print("---STARTING FULL RUN TESTS---\n")   

    print("---starting test_big_problem---\n")
    score, details = test_big_problem(stu_models.hitori_csp_model_1, stu_orderings)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished test_big_problem---\n")

    print("---starting full run model 1---")
    score, details = test_full_run(stu_models.hitori_csp_model_1, stu_orderings)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished full model 1---\n")

    print("---starting full run model 2---")
    score, details = test_full_run(stu_models.hitori_csp_model_2, stu_orderings)
    print(details)
    print("score: %d" % score)
    total_score += score
    print("---finished full run model 2---\n")

    if total_score == TOTAL_POINTS:
        print("Score: %d/%d; Passed all tests" % (total_score,TOTAL_POINTS))
    else:
        print("Score: %d/%d; Did not pass all tests." % (total_score,TOTAL_POINTS))

if __name__=="__main__":
    main()
