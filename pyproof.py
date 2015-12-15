"""	pyproof v.0.11
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
		return "INVALID OPERATION: expression2 must be logical"
		
	def __or__(self, other):
		if isinstance(other, logical):
			return disjunction(self, other)
		return "INVALID OPERATION: expression2 must be logical"
		
	def __rshift__(self, other):
		if isinstance(other, logical):
			return conditional(self, other)
		return "INVALID OPERATION: expression2 must be logical"
		
	def __pow__(self, other):
		if isinstance(other, logical):
			return biconditional(self, other)
		return "INVALID OPERATION: expression2 must me logical"
		
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
	return "INVALID OPERAND: expression1 must be conditional"

def Modus_Tollens(expression1, expression2):
	if isinstance(expression1, conditional):
		if expression2 == negation(expression1[1]):
			return negation(expression1[0])
		return "INVALID OPERATION: Modus Tollens not applicable"
	return "INVALID OPERAND: expression1 must be conditional"

def Hypothetical_Syllogism(expression1, expression2):
	if isinstance(expression1, conditional) and isinstance(expression2, conditional):
		if expression2[0] ==  expression1[1]:
			return conditional(expression1[0], expression2[1])
		return "INVALID OPERATION: Hypothetical Syllogism not applicable"
	return "INVALID OPERAND: expression1 and expression2 must be conditional"

def Disjunctive_Syllogism(expression1, expression2):
	if isinstance(expression1, disjunction) and isinstance(expression2, negation):
		if expression2[0] == expression1[0]:
			return expression1.contents[1]
		return "INVALID OPERATION: Disjunctive Syllogism not applicable"
	return "INVALID OPERAND: expression 1 must be disjunction and expression2 must be negation"

def Constructive_Dilemma(expression1, expression2):
	if isinstance(expression1, conjunction) and isinstance(expression1[0], conditional) and isinstance(expression1[1], conditional) and isinstance(expression2, disjunction):
		if expression2[0] == expression1[0].contents[0] and expression2[1] == expression1[1][0]:
			return disjunction(expression1[0][1], expression1[1][1])
		return "INVALID OPERATION: Constructive Dilemma not applicable"
	return "INVALID OPERAND: expression1 must be conjunction of conditionals and expression2 must be disjunction"

def Simplification(expression1):
	if isinstance(expression1, conjunction):
		return expression1[0]
	return "INVALID OPERAND: expression must be conjunction"

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
class Proof:
	
	def __init__(self):
		self.assumptions = []
		self.theorems = []
		self.justifications = []
		
	def assume(self, expression):
		self.assumptions.append(expression)
		self.justifications.append("")
		self.show()
		
	def mp(self, index1, index2):
		total_list = self.assumptions + self.theorems
		temp = Modus_Ponens(total_list[index1-1], total_list[index2-1])
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("MP " + str(index1) + ", " + str(index2))
			self.show()
			return
		return temp
		
	def mt(self, index1, index2):
		total_list = self.assumptions + self.theorems
		temp = Modus_Tollens(total_list[index1-1], total_list[index2-1])
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("MT " + str(index1) + ", " + str(index2))
			self.show()
			return
		return temp
		
	def hs(self, index1, index2):
		total_list = self.assumptions + self.theorems
		temp = Hypothetical_Syllogism(total_list[index1-1], total_list[index2-1])
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("HS " + str(index1) + ", " + str(index2))
			self.show()
			return
		return temp
		
	def ds(self, index1, index2):
		total_list = self.assumptions + self.theorems
		temp = Disjunctive_Syllogism(total_list[index1-1], total_list[index2-1])
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("DS " + str(index1) + ", " + str(index2))
			self.show()
			return
		return temp
		
	def cd(self, index1, index2):
		total_list = self.assumptions + self.theorems
		temp = Constructive_Dilemma(total_list[index1-1], total_list[index2-1])
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("CD " + str(index1) + ", " + str(index2))
			self.show()
			return
		return temp
		
	def simp(self, index1):
		total_list = self.assumptions + self.theorems
		temp = Simplification(total_list[index1-1])
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("Simp " + str(index1))
			self.show()
			return
		return temp
		
	def conj(self, index1, index2):
		total_list = self.assumptions + self.theorems
		temp = Conjunction(total_list[index1-1], total_list[index2-1])
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("Conj " + str(index1) + ", " + str(index2))
			self.show()
			return
		return temp
		
	def add(self, index1, expression1):
		total_list = self.assumptions + self.theorems
		temp = Addition(total_list[index1-1], expression1)
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("Add " + str(index1))
			self.show()
			return
		return temp
		
	def dm(self, index1):
		total_list = self.assumptions + self.theorems
		temp = DeMorgan(total_list[index1-1])
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("DM " + str(index1))
			self.show()
			return
		return temp
		
	def com(self, index1):
		total_list = self.assumptions + self.theorems
		temp = Commutation(total_list[index1-1])
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("Com " + str(index1))
			self.show()
			return
		return temp
		
	def assoc(self, index1, case = 0):
		total_list = self.assumptions + self.theorems
		temp = Association(total_list[index1-1], case)
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("Assoc " + str(index1))
			self.show()
			return
		return temp
		
	def dist(self, index1, case = 0):
		total_list = self.assumptions + self.theorems
		temp = Distribution(total_list[index1-1], case)
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("Dist " + str(index1))
			self.show()
			return
		return temp
		
	def dn(self, index1, case = 0):
		total_list = self.assumptions + self.theorems
		temp = Double_Negation(total_list[index1-1], case)
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("DN " + str(index1))
			self.show()
			return
		return temp
		
	def trans(self, index1, case = 0):
		total_list = self.assumptions + self.theorems
		temp = Transposition(total_list[index1-1], case)
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("Trans " + str(index1))
			self.show()
			return
		return temp
		
	def impl(self, index1):
		total_list = self.assumptions + self.theorems
		temp = Material_Implication(total_list[index1-1])
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("Impl " + str(index1))
			self.show()
			return
		return temp
		
	def equiv(self, index1, case = 0):
		total_list = self.assumptions + self.theorems
		temp = Material_Equivalence(total_list[index1-1], case)
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("Equiv " + str(index1))
			self.show()
			return
		return temp
		
	def exp(self, index1):
		total_list = self.assumptions + self.theorems
		temp = Exportation(total_list[index1-1])
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("Exp " + str(index1))
			self.show()
			return
		return temp
		
	def taut(self, index1, case = 0):
		total_list = self.assumptions + self.theorems
		temp = Tautology(total_list[index1-1], case)
		if isinstance(temp, logical):
			self.theorems.append(temp)
			self.justifications.append("Taut " + str(index1))
			self.show()
			return
		return temp
		
	def remove(self):
		if len(self.theorems) > 0:
			del self.theorems[-1]
			del self.justifications[-1]
			self.show()
			return
		elif len(self.assumptions) > 0:
			del self.assumptions[-1]
			del self.justifications[-1]
			self.show()
			return
		print("Nothing to remove")
		return
		
	def show(self):
		i = 1
		total_list = self.assumptions + self.theorems
		while i <= (len(total_list)):
			output = str(i) + ".\t" + total_list[i-1].show() + "\t\t\t\t" + self.justifications[i-1]
			print output
			i += 1
