import itertools
'''
This file will contain different constraint propagators to be used within
bt_search.

propagator == a function with the following template
	propagator(csp, newly_instantiated_variable=None)
		==> returns (True/False, [(Variable, Value), (Variable, Value) ...])

Consider implementing propagators for forward cehcking or GAC as a course project!		

'''

def prop_BT(csp, newVar=None):
	'''Do plain backtracking propagation. That is, do no
	propagation at all. Just check fully instantiated constraints'''

	if not newVar:
		return True, []
	for c in csp.get_cons_with_var(newVar):
		if c.get_n_unasgn() == 0:
			vals = []
			vars = c.get_scope()
			for var in vars:
				vals.append(var.get_assigned_value())
			if not c.check(vals):
				return False, []
	return True, []
	
def FC_BT(csp, newVar=None):
	'''Implements Forward Checking
	returns
		status: False if domain wipe out
		prunings: list of pairs: (var, val) that have been pruned'''

	if not newVar:
		return True, []
	prunings = []
	for c in csp.get_cons_with_var(newVar):
		if c.get_n_unasgn() == 1:
			var_unassigned = c.get_unasgn_vars()[0]
			variable_scope = c.get_scope()
			assignments = []
			for var in variable_scope:	
				if var == var_unassigned:
					assignments.append(-1)
				else:
					assignments.append(var.get_assigned_value())
					if assignments[-1] == None:
						print("Error var {} should be assigned".format(var.name))
			status, prunings_constraint = FCCheck(c, var_unassigned, assignments)
			prunings.append(prunings_constraint)
			if not status:
				return False, list(itertools.chain.from_iterable(prunings))
	return True, list(itertools.chain.from_iterable(prunings))

def FCCheck(constraint, var, assignments):
	'''
	inputs:
		constraint: Constraints object from cspbase
		var: Unassigned Variable object in constraint from cspbase
		assignments: List of assignments for each varible in constraint
	returns:
		status: False if DWO
		prunings: list of pairs: (var, val) that have been pruned for this constraint'''
	assignments_index = assignments.index(-1)
	prunings = []
	for pos_assignment in var.cur_domain():
		assignments[assignments_index] = pos_assignment
		if not constraint.check(assignments):
			var.prune_value(pos_assignment)
			prunings.append((var, pos_assignment))
	if var.cur_domain_size() == 0:
		return False, prunings
	return True, prunings