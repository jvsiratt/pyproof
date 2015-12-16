"""	pyproof v.0.19
	proof helper
	currently implemented: first order logic without conditional or indirect proof
	John V Siratt
"""

#parent class for logical connectives
class logical:
	
	left_delimiter = "("
	right_delimiter = ")"
	
	def __init__(self):
		self.string = ''
		self.contents = []
	
	def __invert__(self):
		return negation(self)
		
	def __and__(self, other):
		if isinstance(other, logical):
			return conjunction(self, other)
		return "INVALID INPUT: expression2 must be logical"
		
	def __or__(self, other):
		if isinstance(other, logical):
			return disjunction(self, other)
		return "INVALID INPUT: expression2 must be logical"
		
	def __rshift__(self, other):
		if isinstance(other, logical):
			return conditional(self, other)
		return "INVALID INPUT: expression2 must be logical"
		
	def __pow__(self, other):
		if isinstance(other, logical):
			return biconditional(self, other)
		return "INVALID INPUT: expression2 must me logical"
		
	def __getitem__(self, index):
		return self.contents[index]
		
	def __eq__(self, other):
		if isinstance(other, logical):
			return self.string == other.string
		return False
		
	def __repr__(self):
		return self.string
		
	def __str__(self):
		return self.string
		
	def show(self):
		return self.string
 
class atom(logical):
	
	def __init__(self, label):
		if isinstance(label, str):
			self.string = label
		else:
			return "INVALID INPUT: label must be string"

class negation(logical):
	
	def __init__(self, expression1):
		self.infix = "~"
		if isinstance(expression1, logical):
			self.contents = [expression1]
			self.string = self.left_delimiter + self.infix + self[0].show() + self.right_delimiter
		else:
			return "INVALID INPUT: expression must be logical"

class conjunction(logical):
	
	def __init__(self, expression1, expression2):
		self.infix = "&"
		if isinstance(expression1, logical) and isinstance(expression2, logical):
			self.contents = [expression1, expression2]
			self.string = self.left_delimiter + self[0].show() + self.infix + self[1].show() + self.right_delimiter
		else:
			return "INVALID INPUT: expressions must be logical"
	
class disjunction(logical):
	
	def __init__(self, expression1, expression2):
		self.infix = "|"
		if isinstance(expression1, logical) and isinstance(expression2, logical):
			self.contents = [expression1, expression2]
			self.string = self.left_delimiter + self[0].show() + self.infix + self[1].show() + self.right_delimiter
		else:
			return "INVALID INPUT: expressions must be logical"
	
class conditional(logical):
	
	def __init__(self, expression1, expression2):
		self.infix = ">>"
		if isinstance(expression1, logical) and isinstance(expression2, logical):
			self.contents = [expression1, expression2]
			self.string = self.left_delimiter + self[0].show() + self.infix + self[1].show() + self.right_delimiter
		else:
			return "INVALID INPUT: expressions must be logical"

class biconditional(logical):
	
	def __init__(self, expression1, expression2):
		self.infix = "**"
		if isinstance(expression1, logical) and isinstance(expression2, logical):
			self.contents = [expression1, expression2]
			self.string = self.left_delimiter + self[0].show() + self.infix + self[1].show() + self.right_delimiter
		else:
			return "INVALID INPUT: expressions must be logical"

#implementation of implication rules
def Modus_Ponens(expression1, expression2):
	if isinstance(expression1, conditional):
		if expression2 == expression1[0]:
			return expression1[1]
		return "INVALID OPERATION: Modus Ponens not applicable"
	return "INVALID INPUT: expression1 must be conditional"

def Modus_Tollens(expression1, expression2):
	if isinstance(expression1, conditional):
		if expression2 == negation(expression1[1]):
			return negation(expression1[0])
		return "INVALID OPERATION: Modus Tollens not applicable"
	return "INVALID INPUT: expression1 must be conditional"

def Hypothetical_Syllogism(expression1, expression2):
	if isinstance(expression1, conditional) and isinstance(expression2, conditional):
		if expression2[0] ==  expression1[1]:
			return conditional(expression1[0], expression2[1])
		return "INVALID OPERATION: Hypothetical Syllogism not applicable"
	return "INVALID INPUT: expression1 and expression2 must be conditional"

def Disjunctive_Syllogism(expression1, expression2):
	if isinstance(expression1, disjunction) and isinstance(expression2, negation):
		if expression2[0] == expression1[0]:
			return expression1.contents[1]
		return "INVALID OPERATION: Disjunctive Syllogism not applicable"
	return "INVALID INPUT: expression 1 must be disjunction and expression2 must be negation"

def Constructive_Dilemma(expression1, expression2):
	if isinstance(expression1, conjunction) and isinstance(expression1[0], conditional) and isinstance(expression1[1], conditional) and isinstance(expression2, disjunction):
		if expression2[0] == expression1[0].contents[0] and expression2[1] == expression1[1][0]:
			return disjunction(expression1[0][1], expression1[1][1])
		return "INVALID OPERATION: Constructive Dilemma not applicable"
	return "INVALID INPUT: expression1 must be conjunction of conditionals and expression2 must be disjunction"

def Simplification(expression1):
	if isinstance(expression1, conjunction):
		return expression1[0]
	return "INVALID INPUT: expression must be conjunction"

def Conjunction(expression1, expression2):
	return conjunction(expression1, expression2)

def Addition(expression1, expression2):
	return disjunction(expression1, expression2)


#implementation of replacement rules
def DeMorgan(expression1):
	if isinstance(expression1, negation) and isinstance(expression1[0], conjunction):
		return disjunction(negation(expression1[0][0]), negation(expression1[0][1]))
	elif isinstance(expression1, negation) and isinstance(expression1[0], disjunction):
		return conjunction(negation(expression1[0][0]), negation(expression1[0][1]))
	elif isinstance(expression1, disjunction) and isinstance(expression1[0], negation) and isinstance(expression1[1], negation):
		return negation(conjunction(expression1[0][0], expression1[1][0]))
	elif isinstance(expression1, conjunction) and isinstance(expression1[0], negation) and isinstance(expression1[1], negation):
		return negation(disjunction(expression1[0][0], expression1[1][0]))
	return "INVALID OPERATION: DeMorgan does not apply"
	
def Commutation(expression1):
	if isinstance(expression1, disjunction):
		return disjunction(expression1[1], expression1[0])
	elif isinstance(expression1, conjunction):
		return conjunction(expression1[1], expression1[0])
	return "INVALID OPERATION: Commutation does not apply"
	
def Association(expression1, case = 0):
	if case == 1:
		if isinstance(expression1, disjunction) and isinstance(expression1[1], disjunction):
			return disjunction(disjunction(expression1[0], expression1[1][0]), expression1[1][1])
		elif isinstance(expression1, conjunction) and isinstance(expression1[1], conjunction):
			return conjunction(conjunction(expression1[0], expression1[1][0]), expression1[1][1])
		return "INVALID OPERATION: Associative case [p * (q * r) => (p * q) * r] does not apply"
	if case == 2:
		if isinstance(expression1, disjunction) and isinstance(expression1[0], disjunction):
			return disjunction(expression1[0][0], disjunction(expression1[0][1], expression1[1]))
		elif isinstance(expression1, conjunction) and isinstance(expression1[0], conjunction):
			return conjunction(expression1[0][0], conjunction(expression1[0][1], expression1[1]))
		return "INVALID OPERATION: Associative case [(p * q) * r => p * (q * r)] does not apply"
	else:
		print("1.\tp * (q * r) => (p * q) * r\n2.\t(p * q) * r => p * (q * r)\n")
		return "INVALID INPUT: must select case"
	
def Distribution(expression1, case = 0):
	if case == 1:
		if isinstance(expression1, conjunction) and isinstance(expression1[1], disjunction):
			return disjunction(conjunction(expression1[0], expression1[1][0]), conjunction(expression1[0], expression1[1][1]))
		elif isinstance(expression1, disjunction) and isinstance(expression1[1], conjunction):
			return conjunction(disjunction(expression1[0], expression1[1][0]), disjunction(expression1[0], expression1[1][1]))	
		return "INVALID OPERATION: Distributive case [p * (q x r) => (p * q) x (p * r)] does not apply"
	if case == 2:
		if isinstance(expression1, disjunction) and isinstance(expression1[0], conjunction) and isinstance(expression1[1], conjunction) and expression1[0][0] ==  expression1[1][0]:
			return conjunction(expression1[0][0], disjunction(expression1[0][1], expression1[1][1]))
		elif isinstance(expression1, conjunction) and isinstance(expression1[0], disjunction) and isinstance(expression1[1], disjunction) and expression1[0][0] == expression1[1][0]:
			return disjunction(expression1[0][0], conjunction(expression1[0][1], expression1[1][1]))	
		return "INVALID OPERATION: Distributive case [(p * q) x (p * r) => p * (q x r)] does not apply"
	else:
		print("1.\tp * (q x r) => (p * q) x (p * r)\n2.\t(p * q) x (p * r) => p * (q x r)\n")
		return "INVALID INPUT: must select case"	

def Double_Negation(expression1, case = 0):
	if case == 1:
		return negation(negation(expression1))
	if case == 2:
		if isinstance(expression1, negation) and isinstance(expression1[0], negation):
			return expression1[0][0]
		return "INVALID OPERATION: Double Negative case [~~p => p] does not apply"
	else:
		print("1.\tp => ~~p\n2.\t~~p => p\n")	
		return "INVALID INPUT: must select case"	
		
def Transposition(expression1, case = 0):
	if case == 1:
		if isinstance(expression1, conditional) and isinstance(expression1[0], negation) and isinstance(expression1[1], negation):
			return conditional(expression1[1][0], expression1[0][0])
		return "INVALID OPERATION: Trasposition case [(p >> q) => (~q >> ~p)] does not apply"
	if case == 2:
		if isinstance(expression1, conditional):
			return conditional(negation(expression1[1]), negation(expression1[0]))
		return "INVALID OPERATION: Transposition case [(~q >> ~p) => (p >> q)] does not apply"
	else:
		print("1.\t(p >> q) => (~q >> ~p)\n2.\t(~q >> ~p) => (p >> q)\n")
		return "INVALID INPUT: must select case"
	
def Material_Implication(expression1):
	if isinstance(expression1, conditional):
		return disjunction(negation(expression1[0]), expression1[1])
	elif isinstance(expression1, disjunction) and isinstance(expression1[0], negation):
		return conditional(expression1[0][0], expression1[1])
	return "INVALID OPERATION: Material Implication does not apply"

def Material_Equivalence(expression1, case = 0):
	if case == 1:
		if isinstance(expression1, biconditional):
			return conjunction(conditional(expression1[0], expression1[1]), conditional(expression1[1], expression1[0]))
		return "INVALID OPERATION: Materially Equivalent case [(p ** q) => (p >> q) & (q >> p)] does not apply"
	if case == 2:
		if isinstance(expression1, biconditional):
			return disjunction(conjunction(expression1[0], expression1[1]), conjunction(negation(expression1[0]), negation(expression1[1])))
		return "INVALID OPERATION: Materially Equivalent case [(p ** q) => (p & q) | (~p & ~q)] does not apply"
	if case == 3:
		if isinstance(expression1, conjunction) and isinstance(expression1[0], conditional) and isinstance(expression1[1], conditional) and expression1[0][0] == expression1[1][1] and expression1[0][1] == expression1[1][0]:
			return biconditional(expression1[0][0], expression1[0][1])
		return "INVALID OPERATION: Materially Equivalent case [(p >> q) & (q >> p) => (p ** q)] does not apply"
	if case == 4:#not sure about this case, may lead to problems
		if isinstance(expression1, disjunction) and isinstance(expression1[0], conjunction) and isinstance(expression1[1], conjunction) and expression1[0][0] == expression1[1][0][0] and expression1[0][1] == expression1[1][1][0]:
			return biconditional(expression1[0][0], expression1[0][1])
		return "INVALID OPERATION: Materially Equivalent case [(p & q) | (~p & ~q) => (p ** q)] does not apply"
	else:
		print("1.\t(p ** q) => (p >> q) & (q >> p)\n2.\t(p ** q) => (p & q) | (~p & ~q)\n3.\t(p >> q) & (q >> p) => (p ** q)\n4.\t(p & q) | (~p & ~q) => (p ** q)")
		return "INVALID INPUT: must choose case"
		
'''may run into double negation problem'''
def Exportation(expression1):
	if isinstance(expression1, conditional) and isinstance(expression1[0], conjunction):
		return conditional(expression1[0][0], conditional(expression1[0][1], expression1[1]))
	elif isinstance(expression1, conditional)  and isinstance(expression1[1], conditional):
		return conditional(conjunction(expression1[0], expression1[1].contents[0]), expression1[1][1])
	return "INVALID OPERATION: Exportation does not apply"

def Tautology(expression1, case = 0):
	if case == 1:
		return disjunction(expression1, expression1)
	if case == 2:
		return conjunction(expression1, expression2)
	if case == 3:
		if (isinstance(expression1, conjunction) or isinstance(expression1, disjunction))and expression1[0] == expression1[1]:
			return expression1[0]
		return "INVALID OPERATION: Tautological case [(p * p) => p] does not apply"
	else:
		print("1,\tp => (p | p)\n2.\tp => (p & p)\n3.\t(p * p) => p\n")
		return "INVALID INPUT: must choose case"

#proof object to wrap everything
def iscontradiction(expression):
	if isinstance(expression, conjunction):
		if isinstance(expression[0], negation) and expression[0][0] == expression[1]:
			return True
		if isinstance(expression[1], negation) and expression[0] == expression[1][0]:
			return True
	return False
		
class proof_entry:
	
	def __init__(self):
		self.expression = None
		self.justification = None
		self.recursion = None
		self.string = self.expression.show() + "\t\t\t\t" + self.justification
		
	def show(self):
		return self.string
		
	def __getitem__(self, index):
		return self.expression[index]
		
	def __repr__(self):
		return self.string
		
	def __str__(self):
		return self.string_at
		
class assumption(proof_entry):
	
	def __init__(self, expression):
		self.expression = expression
		self.recursion = []
		self.string = self.expression.show()
		
class theorem(proof_entry):
	
	def __init__(self, expression, justification):
		self.expression = expression
		self.justification = justification
		self.recursion = []
		self.string = self.expression.show() + "\t\t\t\t" + self.justification

class Proof:
	
	def __init__(self):
		self.entries = []
		self.proof_goal = None
	
	def assume(self, expression):
		if not isinstance(expression, logical):
			return "INVALID INPUT: expression must be logical"
		if len(self.entries) == 0 or isinstance(self.entries[-1], assumption):
			self.entries.append(assumption(expression))
			self.show()
			return
		else:
			return "INVALID OPERATION: unable to make further assumptions"

	def goal(self, expression):
		if not isinstance(expression, logical):
			return "INVALID INPUT: expression must be logical"
		self.proof_goal = expression
		self.show()
		return

	def update(self, result, justification):
		last_entry = self.entries[-1]
		if isinstance(result, logical):
			new_entry = theorem(result, justification)
			new_entry.recursion = last_entry.recursion
			self.entries.append(new_entry)
			self.show()
			return
		return result
			
	def scope_test(self, index1, index2):
		current_scope = len(self.entries[-1].recursion)
		called_scope1 = len(self.entries[index1-1].recursion)
		called_scope2 = len(self.entries[index2-1].recursion)
		if called_scope1 >> current_scope or called_scope2 >> current_scope:
			return False
		return True

	def mp(self, index1, index2):
		if self.scope_test(index1, index2) == False:
			return "INVALID OPERATION: out of scope"
		result = Modus_Ponens(self.entries[index1-1].expression, self.entries[index2-1].expression)
		justification = "MP " + str(index1) + ", " + str(index2)
		return self.update(result, justification)
			
	def mt(self, index1, index2):
		if self.scope_test(index1, index2) == False:
			return "INVALID OPERATION: out of scope"
		result = Modus_Tollens(self.entries[index1-1].expression, self.entries[index2-1].expression)
		justification = "MT " + str(index1) + ", " + str(index2)
		return self.update(result, justification)
		
	def hs(self, index1, index2):
		if self.scope_test(index1, index2) == False:
			return "INVALID OPERATION: out of scope"
		result = Hypothetical_Syllogism(self.entries[index1-1].expression, self.entries[index2-1].expression)
		justification = "HS " + str(index1) + ", " + str(index2)
		return self.update(result, justification)

	def ds(self, index1, index2):
		if self.scope_test(index1, index2) == False:
			return "INVALID OPERATION: out of scope"
		result = Disjunctive_Syllogism(self.entries[index1-1].expression, self.entries[index2-1].expression)
		justification = "DS " + str(index1) + ", " + str(index2)
		return self.update(result, justification)
		
	def cd(self, index1, index2):
		if self.scope_test(index1, index2) == False:
			return "INVALID OPERATION: out of scope"
		result = Constructive_Dilemma(self.entries[index1-1].expression, self.entries[index2-1].expression)
		justification = "CD " + str(index1) + ", " + str(index2)
		return self.update(result, justification)

	def simp(self, index1):
		if self.scope_test(index1, index1) == False:
			return "INVALID OPERATION: out of scope"
		result = Simplification(self.entries[index1-1].expression)
		justification = "Simp " + str(index1)
		return self.update(result, justification)

	def conj(self, index1, index2):
		if self.scope_test(index1, index2) == False:
			return "INVALID OPERATION: out of scope"
		result = Conjunction(self.entries[index1-1].expression, self.entries[index2-1].expression)
		justification = "Conj " + str(index1) + ", " + str(index2)
		return self.update(result, justification)

	def add(self, index1, expression1):
		if self.scope_test(index1, index1) == False:
			return "INVALID OPERATION: out of scope"
		result = Addition(self.entries[index1-1].expression, expression1)
		justification = "Add " + str(index1)
		return self.update(result, justification)

	def dm(self, index1):
		if self.scope_test(index1, index1) == False:
			return "INVALID OPERATION: out of scope"
		result = DeMorgan(self.entries[index1-1].expression)
		justification = "DM " + str(index1)
		return self.update(result, justification)

	def com(self, index1):
		if self.scope_test(index1, index1) == False:
			return "INVALID OPERATION: out of scope"
		result = Commutation(self.entries[index1-1].expression)
		justification = "Com " + str(index1)
		return self.update(result, justification)
		
	def assoc(self, index1, case = 0):
		if self.scope_test(index1, index1) == False:
			return "INVALID OPERATION: out of scope"
		result = Association(self.entries[index1-1].expression, case)
		justification = "Assoc " + str(index1)
		return self.update(result, justification)

	def dist(self, index1, case = 0):
		if self.scope_test(index1, index1) == False:
			return "INVALID OPERATION: out of scope"
		result = Distribution(self.entries[index1-1].expression, case)
		justification = "Dist " + str(index1)
		return self.update(result, justification)

	def dn(self, index1, case = 0):
		if self.scope_test(index1, index1) == False:
			return "INVALID OPERATION: out of scope"
		result = Double_Negation(self.entries[index1-1].expression, case)
		justification = "DN " + str(index1)
		return self.update(result, justification)

	def trans(self, index1, case = 0):
		if self.scope_test(index1, index1) == False:
			return "INVALID OPERATION: out of scope"
		result = Transposition(self.entries[index1-1].expression, case)
		justification = "Trans " + str(index1)
		return self.update(result, justification)

	def impl(self, index1):
		if self.scope_test(index1, index1) == False:
			return "INVALID OPERATION: out of scope"
		result = Material_Implication(self.entries[index1-1].expression)
		justification = "Impl " + str(index1)
		return self.update(result, justification)

	def equiv(self, index1, case = 0):
		if self.scope_test(index1, index1) == False:
			return "INVALID OPERATION: out of scope"
		result = Material_Equivalence(self.entries[index1-1].expression, case)
		justification = "Equiv " + str(index1)
		return self.update(result, justification)

	def exp(self, index1):
		if self.scope_test(index1, index1) == False:
			return "INVALID OPERATION: out of scope"
		result = Exportation(self.entries[index1-1].expression)
		justification = "Exp " + str(index1)
		return self.update(result, justification)

	def taut(self, index1, case = 0):
		if self.scope_test(index1, index1) == False:
			return "INVALID OPERATION: out of scope"
		result = Tautology(self.entries[index1-1].expression, case)
		justification = "Taut " + str(index1)
		return self.update(result, justification)
		
	def cp(self, expression):
		if isinstance(expression, logical):
			last_entry = self.entries[-1]
			justification = "Assumption (CP)"
			new_entry = theorem(expression, justification)
			new_entry.recursion = last_entry.recursion + ["c"]
			self.entries.append(new_entry)
			self.show()
			return
		return "INVALID INPUT: expression must be logical"
		
	def ip(self, expression):
		if isinstance(expression, logical):
			last_entry = self.entries[-1]
			justification = "Assumption (IP)"
			new_entry = theorem(expression, justification)
			new_entry.recursion = last_entry.recursion + ["i"]
			self.entries.append(new_entry)
			self.show()
			return
		return "INVALID INPUT: expression must be logical"

		
	def discharge(self):
		last_entry = self.entries[-1]
		if len(last_entry.recursion) == 0:
			return "INVALID OPERATION: nothing to discharge"
		if last_entry.recursion[-1] == "c":
			i = 2
			while len(self.entries[-i].recursion) >= len(last_entry.recursion):
				i +=1
			antecedent = self.entries[1-i].expression
			consequent = last_entry.expression
			result = conditional(antecedent, consequent)
			justification = "CP " + str(len(self.entries)-i+2) + " - " + str(len(self.entries))
			new_entry = theorem(result, justification)
			new_entry.recursion = last_entry.recursion[0:-1]
			self.entries.append(new_entry)
			self.show()
			return
		if last_entry.recursion[-1] == "i":
			if iscontradiction(last_entry.expression):
				i = 2
				while len(self.entries[-i].recursion) == len(last_entry.recursion):
					i +=1
				assumpt = self.entries[1-i].expression
				result = negation(assumpt)
				justification = "IP " + str(len(self.entries)-i+2) + " - " + str(len(self.entries))
				new_entry = theorem(result, justification)
				new_entry.recursion = last_entry.recursion[0:-1]
				self.entries.append(new_entry)
				self.show()
				return
		return "INVALID OPERATION: unable to discharge"
		
	def remove(self):
		if len(self.entries) > 0:
			del self.entries[-1]
			self.show()
			return
		return "INVALID OPERATION: nothing to remove"
	
	def show(self):
		i = 1
		while i <= len(self.entries):
			output = len(self.entries[i-1].recursion)*"|" + str(i) + ".\t" + self.entries[i-1].show()
			if isinstance(self.entries[i-1], assumption) and (i == len(self.entries) or isinstance(self.entries[i], theorem)):
				if isinstance(self.proof_goal, logical):
					output = output + "\t\t/" + self.proof_goal.show()
			if isinstance(self.entries[i-2], assumption) and isinstance(self.entries[i-1], theorem):
				print(30*"=")
			print output
			if self.entries[i-1].expression == self.proof_goal and len(self.entries[i-1].recursion) == 0:
				print("QED")
			i += 1
