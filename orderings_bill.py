#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random
import propagators
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
    min_domain_size = 1000
    min_var = None
    #For every unassigned variable
    for var in csp.get_all_unasgn_vars():
      #Find the minimum domain size
      if var.cur_domain_size() < min_domain_size:
        min_var = var
        min_domain_size = var.cur_domain_size()
    return min_var
    
#IMPLEMENT


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
    
    results = []
    #For all unassigned values
    for var in csp.get_all_unasgn_vars():
      checked_list = []
      #Find associated constraints
      for cons in csp.get_cons_with_var(var):
        #Find all variables associated with the constraint
        for constrained_var in cons.get_scope():
          #If not the original variable, not assigned, and not checked previously, add to a list
          if constrained_var != var and constrained_var not in checked_list and not constrained_var.is_assigned():
            checked_list.append(constrained_var)
      #Record how many edges the variable had      
      results.append((var,len(checked_list)))
    #Sort and return the max
    results_sorted = sorted(results, key=lambda x: x[1])
    var = results_sorted[-1][0]
    return var
#IMPLEMENT




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
    results = []
    checked_list = {}
    #For all values the variable can take on
    for val in var.cur_domain(): 
      #For all the constraints that are affected by the value
      for cons in csp.get_cons_with_var(var):
        #If the value for the variable can lead to a solution, continue
        if (var, val) in cons.sup_tuples: 
          #For all the possible assignments with var = val
          for tup in cons.sup_tuples[(var,val)]:
            #Create a dictionary of variables that are affected and the values that they can take on
            for i, scope_val in enumerate(tup):
              # find the associated variable
              scope_var = cons.get_scope()[i]
              # skip self and assigned variables
              if scope_var is not var and not scope_var.is_assigned():
                if (scope_var not in checked_list.keys()):
                  checked_list[scope_var] = []
                if scope_val not in checked_list[scope_var]:
                  checked_list[scope_var].append(scope_val)
      terms_elim = 0
      #Terms eliminated is equal to the difference between the current domain and the previously calculated value
      for scope_var, list_of_vals in checked_list.items():
        terms_elim += scope_var.cur_domain_size() - len(list_of_vals)
      results.append((val,terms_elim))
    results_sorted = sorted(results, key=lambda x: x[1])
    results = [x[0] for x in results_sorted]
    return results
    
#IMPLEMENT


def ord_custom(csp):
    '''
    ord_custom(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to a Heuristic of your design.  This can be a combination of the ordering heuristics 
    that you have defined above.
    '''    
    mrv_vars = []
    min_domain_size = 1000
    min_var = None
    #For every unassigned variable
    for var in csp.get_all_unasgn_vars():
      #Find the minimum domain size
      if var.cur_domain_size() < min_domain_size:
        min_domain_size = var.cur_domain_size()
    #Find all variables with minimum domain size    
    for var in csp.get_all_unasgn_vars():
      if var.cur_domain_size() == min_domain_size:
        mrv_vars.append(var)
    #If only one, return and end
    if len(mrv_vars) == 1:
      return mrv_vars[0]
    #If more than one, use DH to break ties
    results = []
    #For all unassigned values
    for var in mrv_vars:
      checked_list = []
      #Find associated constraints
      for cons in csp.get_cons_with_var(var):
        #Find all variables associated with the constraint
        for constrained_var in cons.get_scope():
          #If not the original variable, not assigned, and not checked previously, add to a list
          if constrained_var != var and constrained_var not in checked_list and not constrained_var.is_assigned():
            checked_list.append(constrained_var)
      #Record how many edges the variable had      
      results.append((var,len(checked_list)))
    #Sort and return the max
    results_sorted = sorted(results, key=lambda x: x[1])
    var = results_sorted[-1][0]
    return var
#IMPLEMENT


