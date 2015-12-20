"""implementation of logical objects"""

from . import *

#parent class for logical objects
class logical:
	
	left_delimiter = "("
	right_delimiter = ")"
	
	def __init__(self):
		self.string = ''
		self.contents = []
		
	#overloading the ~ operator to perform negation
	def __invert__(self):
		return negation(self)
		
	#overloading the & operator to perform conjunciton
	def __and__(self, other):
		if isinstance(other, logical):
			return conjunction(self, other)
		return "INVALID INPUT: expression2 must be logical"
		
	#overloading the | operator to perform disjunction
	def __or__(self, other):
		if isinstance(other, logical):
			return disjunction(self, other)
		return "INVALID INPUT: expression2 must be logical"
		
	#overloading the >> operator to perform conditional
	def __rshift__(self, other):
		if isinstance(other, logical):
			return conditional(self, other)
		return "INVALID INPUT: expression2 must be logical"
		
	#overloading the ** operator to perform material equivalence
	def __pow__(self, other):
		if isinstance(other, logical):
			return biconditional(self, other)
		return "INVALID INPUT: expression2 must me logical"
		
	#indexing returns entries in contents variable
	def __getitem__(self, index):
		return self.contents[index]
		
	#comparison compares string identifiers
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

#atomic object is a logical constant
class atom(logical):
	
	def __init__(self, label):
		if isinstance(label, str):
			self.string = label
		else:
			return "INVALID INPUT: label must be string"

#constanct object
class constant(atom):
	pass

#variables assumed to have some quality
class constrained_variable(atom):
	pass
	
#completely arbitrary variables, typically from Universial Instantiation
class arbitrary_variable(atom):
	pass

#unary connective NOT
class negation(logical):
	
	def __init__(self, expression1):
		self.infix = "~"
		if isinstance(expression1, logical):
			self.contents = [expression1]
			self.string = self.left_delimiter + self.infix + self[0].show() + self.right_delimiter
		else:
			return "INVALID INPUT: expression must be logical"

#binary connective AND
class conjunction(logical):
	
	def __init__(self, expression1, expression2):
		self.infix = "&"
		if isinstance(expression1, logical) and isinstance(expression2, logical):
			self.contents = [expression1, expression2]
			self.string = self.left_delimiter + self[0].show() + self.infix + self[1].show() + self.right_delimiter
		else:
			return "INVALID INPUT: expressions must be logical"

#binary connective OR
class disjunction(logical):
	
	def __init__(self, expression1, expression2):
		self.infix = "|"
		if isinstance(expression1, logical) and isinstance(expression2, logical):
			self.contents = [expression1, expression2]
			self.string = self.left_delimiter + self[0].show() + self.infix + self[1].show() + self.right_delimiter
		else:
			return "INVALID INPUT: expressions must be logical"

#binary connective IF-THEN
class conditional(logical):
	
	def __init__(self, expression1, expression2):
		self.infix = ">>"
		if isinstance(expression1, logical) and isinstance(expression2, logical):
			self.contents = [expression1, expression2]
			self.string = self.left_delimiter + self[0].show() + self.infix + self[1].show() + self.right_delimiter
		else:
			return "INVALID INPUT: expressions must be logical"

#binary connective IFF
class biconditional(logical):
	
	def __init__(self, expression1, expression2):
		self.infix = "**"
		if isinstance(expression1, logical) and isinstance(expression2, logical):
			self.contents = [expression1, expression2]
			self.string = self.left_delimiter + self[0].show() + self.infix + self[1].show() + self.right_delimiter
		else:
			return "INVALID INPUT: expressions must be logical"

#abstract connective between arbitray atoms?
class predicate(logical):
	
	def __init__(self, *args):
		if len(args) < 2:
			return "INVALID INPUT: predicate must contain label and at least one expression"
		if isinstance(args[0], str):
			self.label = label
		else:
			return "INVALID INPUT: label must be string"
		self.contents = []
		for i in range(1, len(args)):
			if isinstance(args[i], logical):
				#should the predicate label be in contents?
				self.contents.append(args[i])
			else:
				return "INVALID INPUT: expressions must be logical"
		self.string = "temp"

#expression containing bound variable of universal quality
class forall(logical):
	
	def __init__(self, variable, expression1):
		if isinstance(variable, arbitrary variable) and isinstance(expression1, logical):
			self.contents = [variable, expression1]
		else:
			return "INVALID INPUT: variable must be arbitrary and expression must be logical"

#expression containing bound variable of existential quality		
class exists(logical):
	
	def __init__(self, variable, expression1):
		if isinstance(variable, arbitrary variable) and isinstance(expression1, logical):
			self.contents = [variable, expression1]
		else:
			return "INVALID INPUT: variable must be arbitrary and expression must be logical"
