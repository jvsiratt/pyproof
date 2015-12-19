"""implementation of proof object"""

from . import *

#helper function for conditional proofing, determines if a contradiction has been reached
def iscontradiction(expression):
	if isinstance(expression, conjunction):
		if isinstance(expression[0], negation) and expression[0][0] == expression[1]:
			return True
		if isinstance(expression[1], negation) and expression[0] == expression[1][0]:
			return True
	return False

#modular container parent class for a line of proof information
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

#entry containing a declared given
class assumption(proof_entry):
	
	def __init__(self, expression):
		self.expression = expression
		self.recursion = []
		self.string = self.expression.show()
	
#entry containing a derived truth	
class theorem(proof_entry):
	
	def __init__(self, expression, justification):
		self.expression = expression
		self.justification = justification
		self.recursion = []
		self.string = self.expression.show() + "\t\t\t\t" + self.justification

#proof container class, includes methods to interface with implication and replacement rules
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
