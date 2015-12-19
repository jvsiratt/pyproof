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

