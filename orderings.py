import random

'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    ord_type(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    ord_type returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''


def ord_random(csp):
    '''
    ord_random(csp):
    A var_ordering function that takes a CSP object csp and returns a Variable object var at random.  var must be an unassigned variable.
    '''
    var = random.choice(csp.get_all_unasgn_vars())
    return var


def val_arbitrary(csp,var):
    '''
    val_arbitrary(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a value in var's current domain arbitrarily.
    '''
    return var.cur_domain()


def ord_mrv(csp):
    '''
    ord_mrv(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var, 
    according to the Minimum Remaining Values (MRV) heuristic as covered in lecture.  
    MRV returns the variable with the most constrained current domain 
    (i.e., the variable with the fewest legal values).
    '''

    unassigned_vars = csp.get_all_unasgn_vars()
    mrv_var = False
    mrv = 100000000000000                   # a very large number to represent infinity

    for unassigned_var in unassigned_vars:
        cur_domain_size = unassigned_var.cur_domain_size()
        if ( cur_domain_size == 1 ):
            return unassigned_var           # this value is forced, propagate immediately
        elif ( cur_domain_size < mrv ):
            mrv_var = unassigned_var
            mrv = cur_domain_size

    return mrv_var


def ord_dh(csp):
    '''
    ord_dh(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to the Degree Heuristic (DH), as covered in lecture.
    Given the constraint graph for the CSP, where each variable is a node, 
    and there exists an edge from two variable nodes v1, v2 iff there exists
    at least one constraint that includes both v1 and v2,
    DH returns the variable whose node has highest degree.
    '''    
    # get all the unassigned variables
    unassigned_vars = csp.get_all_unasgn_vars()
    max_constraints = dict()

    # for each unassigned variable
    for unassigned_var in unassigned_vars:
        # get associated constraints
        constraints = csp.get_cons_with_var(unassigned_var)
        # keep a list of variables that are constrained by this one
        constrained_vars = []
        # for each associated constraint
        for constraint in constraints:
            # for each variable in the same scope
            for var in constraint.get_scope():
                # don't count self or vars that have assigned values
                if ((var is unassigned_var) or (var not in unassigned_vars)):
                    continue
                # add it to the list of constrained variables
                if var not in constrained_vars:
                    constrained_vars.append(var)
            # performance enhancer: check if we have the max possible list size already, break if so
            if (len(constrained_vars) == (len(unassigned_vars) - 1)):
                break
        # add to dict: key is unassigned var, value is number of other variables constrainted by it
        max_constraints[unassigned_var] = len(constrained_vars)

    # return var which imposes the most constraints on other unassigned vars
    return max(max_constraints, key=max_constraints.get)

def val_lcv(csp,var):
    '''
    val_lcv(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a list of Values [val1,val2,val3,...]
    from var's current domain, ordered from best to worst, evaluated according to the 
    Least Constraining Value (LCV) heuristic.
    (In other words, the list will go from least constraining value in the 0th index, 
    to most constraining value in the $j-1$th index, if the variable has $j$ current domain values.) 
    The best value, according to LCV, is the one that rules out the fewest domain values in other 
    variables that share at least one constraint with var.
    '''
    # get all the unassigned variables
    unassigned_vars = csp.get_all_unasgn_vars()

    constraint_sums = dict()                    # keep track of remaining options with dict
    constraints = csp.get_cons_with_var(var)    # get all associated constraints of var
    cur_dom = var.cur_domain()                  # get all possible values for var

    # for each possible value of var
    for value in cur_dom:
        # create a dict that keeps track of which values from other vars' domains are still valid
        other_var_domain = dict()
        # for each constraint associated with this variable
        for constraint in constraints:
            # don't continue if var=value is not in any valid solution
            if (var, value) not in constraint.sup_tuples:
                continue
            # for each assignment tuple which includes var=value
            for t in constraint.sup_tuples[(var, value)]:
                # make sure this tuple is still valid before counting it
                if not constraint.tuple_is_valid(t):
                    continue
                # for each of the other values in the tuple
                for scope_var_index, scope_var_value in enumerate(t):
                    # find the corresponding variable
                    scope_var = constraint.get_scope()[scope_var_index]
                    # skip if self or assigned variable
                    if (var is scope_var) or (scope_var not in unassigned_vars):
                        continue
                    # create a new entry in the dict for scope_var
                    if scope_var not in other_var_domain.keys():
                        other_var_domain[scope_var] = []
                    # add scope_var_value to scope_var's dict entry
                    if scope_var_value not in other_var_domain[scope_var]:
                        other_var_domain[scope_var].append(scope_var_value)

        # done looking at all the constraints, should now have a dict with a list of values
        # for each unassigned variable constrained by var
        eliminated_sum = 0
        for scope_var in other_var_domain:
            # the num of eliminated values can be found by subtracting the length of our
            # valid-values list from the scope_var's current domain size
            eliminated_sum += scope_var.cur_domain_size() - len(other_var_domain[scope_var])

        # store this sum in a dict and then go on to the next value
        constraint_sums[value] = eliminated_sum

    # sort the values in ascending order since we want value which will eliminate the least
    # amount of domain values from other unassigned variables
    sorted_sums = sorted(constraint_sums, key=constraint_sums.get)
    return sorted_sums

def ord_custom(csp):
    '''
    ord_custom(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to a Heuristic of your design.  This can be a combination of the ordering heuristics 
    that you have defined above.
    '''    

    # Try MRV to figure out which variable to assign first
    unassigned_vars = csp.get_all_unasgn_vars()
    mrv = 100000000000000                   # a very large number to represent infinity
    mrv_vars = []                           # a list to store the MRV var(s)

    for unassigned_var in unassigned_vars:
        cur_domain_size = unassigned_var.cur_domain_size()
        if ( cur_domain_size > mrv ):
            continue                        # we don't care about vars with larger current domain sizes
        if ( cur_domain_size < mrv ):
            mrv_vars.clear()                # clear the list if new min domain size found
        mrv_vars.append(unassigned_var)     # add the var to the list
        mrv = cur_domain_size               # set the new minimum domain size

    if ( len(mrv_vars) == 1 ):
        return mrv_vars[0]              # return if we found a single match

    # Do tie-breaking with DH
    max_constraints = dict()

    for mrv_var in mrv_vars:
        constraints = csp.get_cons_with_var(mrv_var)
        constrained_vars = []
        # collect all the other vars that this var puts constraints on
        for constraint in constraints:
            for var in constraint.get_scope():
                # don't count self or vars that have assigned values
                if ((var is mrv_var) or (var not in unassigned_vars)):
                    continue
                # keep a unique list
                if var not in constrained_vars:
                    constrained_vars.append(var)
            # performance enhancer: check if we have the max possible list size already, break if so
            if (len(constrained_vars) == (len(unassigned_vars) - 1)):
                break
        max_constraints[mrv_var] = len(constrained_vars)

    return max(max_constraints, key=max_constraints.get)