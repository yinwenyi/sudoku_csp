'''
Construct and return sudoku CSP models.
'''

from cspbase import *
import itertools

def sudoku_csp_model(initial_sudoku_board):
    '''Return a CSP object representing a sudoku CSP problem along 
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudoku board (indexed from (0,0) to (8,8))
       
       The input board is specified as a list of n lists. Each of the
       n lists represents a row of the board. Each item in the list 
       represents a cell, and will contain a number between 1-9 or 0,
       where 0 represents a blank square.
   
       The variables of model_2 are: a variable for each cell of the board,
       with domain equal to {1,2,3,4,5,6,7,8,9} for unassigned vars.
       Assigned vars have a domain of {i}, where i is the initial value.
       Variables will be named '0-0' through '8-8'.

       model has 27 all-different constraints, 9 for the rows, 9 for the
       columns, and 9 for the subgrids. Each constraint is over 9 variables.
       
    '''
    sudoku_csp = CSP("sudoku_csp_model")

    # initialize nested list for array of variables
    variable_array = [[None for x in range(len(initial_sudoku_board))] for x in range(len(initial_sudoku_board))]

    # initialize and add all variables
    for i in range(len(initial_sudoku_board)):
        for j in range(len(initial_sudoku_board)):
            var_name = str(i) + "-" + str(j)
            curr_var = Variable(var_name)
            if initial_sudoku_board[i][j] != 0: # value already assigned
                curr_var.add_domain_values([initial_sudoku_board[i][j]])
            else:
                curr_var.add_domain_values([1,2,3,4,5,6,7,8,9])
            sudoku_csp.add_var(curr_var)
            # add to the variable array
            variable_array[i][j] = curr_var

    # add the constraints
    # go through the rows first
    for row in range(len(initial_sudoku_board)):
        constr_name = "R," + str(row)
        constraint = Constraint(constr_name, variable_array[row])
        sat_tuples = gen_constraint_tuples(variable_array[row], len(initial_sudoku_board))
        constraint.add_satisfying_tuples(sat_tuples)
        sudoku_csp.add_constraint(constraint)

    # then go through the columns
    for col in range(len(initial_sudoku_board)):
        constr_name = "C," + str(col)
        col_vars = column(variable_array, col)
        constraint = Constraint(constr_name, col_vars)
        sat_tuples = gen_constraint_tuples(col_vars, len(initial_sudoku_board))
        constraint.add_satisfying_tuples(sat_tuples)
        sudoku_csp.add_constraint(constraint)

    # finally go through the subgrids
    for sub in range(len(initial_sudoku_board)):
        constr_name = "S," + str(sub)
        sub_vars = subgrid(variable_array, sub)
        constraint = Constraint(constr_name, sub_vars)
        sat_tuples = gen_constraint_tuples(sub_vars, len(initial_sudoku_board))
        constraint.add_satisfying_tuples(sat_tuples)
        sudoku_csp.add_constraint(constraint)

    return sudoku_csp, variable_array

def column(array, i):
    '''
    Returns a list of the elements in column i of nested list array
    :param array: nested list
    :param i: int
    :return: list
    '''
    return [row[i] for row in array]

def subgrid(array, index):
    '''
    Returns a list of the elements in subgrid i of nested list array
    The subgrids are as follows:
    |0|1|2|
    |3|4|5|
    |6|7|8|
    Where each subgrid is a 3x3 grid.

    0  1  2   3  4  5   6  7  8
    9  10 11  12 13 14  15 16 17
    18 19 20  21 22 23  24 25 26

    27 28 29  30 31 32  33 34 35
    36 37 38  39 40 41  42 43 44
    45 46 47  48 49 50  51 52 53

    54 55 56  57 58 59  60 61 62
    63 64 65  66 67 68  69 70 71
    72 73 74  75 76 77  78 79 80

    :param array: nested list
    :param index: int
    :return: list
    '''
    size = 3
    x = index / size   # the 'row' the subgrid is in
    y = index % size   # the 'col' the subgrid is in

    var_list = []
    # figure out the index of the top leftmost element
    topleft = x*27 + y*3
    midleft = topleft + 9
    botleft = midleft + 9

    for i in range(topleft, topleft+3):
        var_list.append(array[i])
    for i in range(midleft, midleft+3):
        var_list.append(array[i])
    for i in range(botleft, botleft+3):
        var_list.append(array[i])

    return var_list

def gen_constraint_tuples(vars, n):
    '''
    Returns a list of n-tuples that satisfy the all-diff constraint.
    Use brute force to go through all possible domain values for each
    variable, ignoring tuples which have duplicates
    :param vars: list of Variables
    :param n: int
    :return: list of n-tuples
    '''

    all_tuples = []
    # safe to use permanent domain values for initial constraints
    for i0 in vars[0].domain():
        for i1 in vars[1].domain():
            for i2 in vars[2].domain():
                for i3 in vars[3].domain():
                    for i4 in vars[4].domain():
                        for i5 in vars[5].domain():
                            for i6 in vars[6].domain():
                                for i7 in vars[7].domain():
                                    for i8 in vars[8].domain():
                                        tup = [i0, i1, i2, i3, i4, i5, i6, i7, i8]
                                        # don't consider any tuples with duplicates
                                        # a set has only unique elements
                                        if len(tup) == len(set(tup)):
                                            all_tuples.append(tuple(tup))
    return all_tuples

########################################################################################################################

def sudoku_csp_model_gac(initial_sudoku_board):
    '''Return a CSP object representing a sudoku CSP problem along
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudoku board (indexed from (0,0) to (8,8))

       The input board is specified as a list of n lists. Each of the
       n lists represents a row of the board. Each item in the list
       represents a cell, and will contain a number between 1-9 or 0,
       where 0 represents a blank square.

       The variables of model_gac are: a variable for each cell of the board,
       with domain equal to {1,2,3,4,5,6,7,8,9} for unassigned vars.
       Assigned vars have a domain of {i}, where i is the initial value.
       Variables will be named '0-0' through '8-8'.

       model_gac has 27 all-different constraints, 9 for the rows, 9 for the
       columns, and 9 for the subgrids. Each constraint is over 9 variables.

       This model enforces GAC on the constraints.

    '''
    sudoku_csp = CSP("sudoku_csp_model_gac")

    # initialize nested list for array of variables
    variable_array = [[None for x in range(len(initial_sudoku_board))] for x in range(len(initial_sudoku_board))]

    # initialize and add all variables
    for i in range(len(initial_sudoku_board)):
        for j in range(len(initial_sudoku_board)):
            var_name = str(i) + "-" + str(j)
            curr_var = Variable(var_name)
            if initial_sudoku_board[i][j] != 0:  # value already assigned
                curr_var.add_domain_values([initial_sudoku_board[i][j]])
            else:
                curr_var.add_domain_values([1, 2, 3, 4, 5, 6, 7, 8, 9])
            sudoku_csp.add_var(curr_var)
            # add to the variable array
            variable_array[i][j] = curr_var

    # add the constraints
    # go through the rows first
    for row in range(len(initial_sudoku_board)):
        constr_name = "R," + str(row)
        constraint = Constraint(constr_name, variable_array[row])
        sat_tuples = gen_constraint_tuples(variable_array[row], len(initial_sudoku_board))
        constraint.add_satisfying_tuples(sat_tuples)
        sudoku_csp.add_constraint(constraint)

    # then go through the columns
    for col in range(len(initial_sudoku_board)):
        constr_name = "C," + str(col)
        col_vars = column(variable_array, col)
        constraint = Constraint(constr_name, col_vars)
        sat_tuples = gen_constraint_tuples(col_vars, len(initial_sudoku_board))
        constraint.add_satisfying_tuples(sat_tuples)
        sudoku_csp.add_constraint(constraint)

    # finally go through the subgrids
    for sub in range(len(initial_sudoku_board)):
        constr_name = "S," + str(sub)
        sub_vars = subgrid(variable_array, sub)
        constraint = Constraint(constr_name, sub_vars)
        sat_tuples = gen_constraint_tuples(sub_vars, len(initial_sudoku_board))
        constraint.add_satisfying_tuples(sat_tuples)
        sudoku_csp.add_constraint(constraint)

    dwo = gac_enforce(sudoku_csp)
    if dwo:
        print("DWO occurred!")

    return sudoku_csp, variable_array

def gac_enforce(sudoku_csp):
    '''
    Enforces GAC on the given CSP.
    The pruned values will be removed from the variable object's cur_domain.
    If a DWO is detected.
    :param sudoku_csp:
    :return: 1 if DWO, else returns 0
    '''

    # begin with all constraints on gac queue
    gac_queue = sudoku_csp.get_all_cons()

    while len(gac_queue) > 0:
        const = gac_queue.pop(0)
        vars = const.get_scope()
        for var in vars:
            domain = var.cur_domain()
            for val in domain:
                # if there isn't a support for var=val, prune val from var's domain
                if not const.has_support(var, val):
                    var.prune_value(val)
                    if len(var.cur_domain()) == 0:  # domain wipe out
                        gac_queue.clear()
                        return 1
                    else:
                        relatedConstraints = sudoku_csp.get_cons_with_var(var)
                        relatedConstraints.remove(const)
                        for relConst in relatedConstraints:
                            if relConst not in gac_queue:   # add all related constraints to the queue
                                gac_queue.append(relConst)
    return 0