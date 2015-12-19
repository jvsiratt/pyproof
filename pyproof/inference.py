"""implementation of implication rules"""

from . import *

#If A&B and A, then B
def Modus_Ponens(expression1, expression2):
	if isinstance(expression1, conditional):
		if expression2 == expression1[0]:
			return expression1[1]
		return "INVALID OPERATION: Modus Ponens not applicable"
	return "INVALID INPUT: expression1 must be conditional"

#If A&B and ~B, then ~A
def Modus_Tollens(expression1, expression2):
	if isinstance(expression1, conditional):
		if expression2 == negation(expression1[1]):
			return negation(expression1[0])
		return "INVALID OPERATION: Modus Tollens not applicable"
	return "INVALID INPUT: expression1 must be conditional"

#If A>>B and B>>C, then A>>C
def Hypothetical_Syllogism(expression1, expression2):
	if isinstance(expression1, conditional) and isinstance(expression2, conditional):
		if expression2[0] ==  expression1[1]:
			return conditional(expression1[0], expression2[1])
		return "INVALID OPERATION: Hypothetical Syllogism not applicable"
	return "INVALID INPUT: expression1 and expression2 must be conditional"

#If A|B and ~A, then B
def Disjunctive_Syllogism(expression1, expression2):
	if isinstance(expression1, disjunction) and isinstance(expression2, negation):
		if expression2[0] == expression1[0]:
			return expression1.contents[1]
		return "INVALID OPERATION: Disjunctive Syllogism not applicable"
	return "INVALID INPUT: expression 1 must be disjunction and expression2 must be negation"

#If (A>>B)&(C>>D) and A|C, then B|D
def Constructive_Dilemma(expression1, expression2):
	if isinstance(expression1, conjunction) and isinstance(expression1[0], conditional) and isinstance(expression1[1], conditional) and isinstance(expression2, disjunction):
		if expression2[0] == expression1[0].contents[0] and expression2[1] == expression1[1][0]:
			return disjunction(expression1[0][1], expression1[1][1])
		return "INVALID OPERATION: Constructive Dilemma not applicable"
	return "INVALID INPUT: expression1 must be conjunction of conditionals and expression2 must be disjunction"

#If A&B then A
def Simplification(expression1):
	if isinstance(expression1, conjunction):
		return expression1[0]
	return "INVALID INPUT: expression must be conjunction"

#If A and B, then A&B
def Conjunction(expression1, expression2):
	return conjunction(expression1, expression2)

#If A, then A|X
def Addition(expression1, expression2):
	return disjunction(expression1, expression2)


"""implementation of replacement rules"""
#distribution of negation over conjunction and disjunction
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

#commutivity of conjunction and disjunction
def Commutation(expression1):
	if isinstance(expression1, disjunction):
		return disjunction(expression1[1], expression1[0])
	elif isinstance(expression1, conjunction):
		return conjunction(expression1[1], expression1[0])
	return "INVALID OPERATION: Commutation does not apply"

#associativity of conjunction and disjunction
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
	
#distribution of conjunction and disjunction
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

#If A iff ~~A
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

#If A>>B, then ~B>>~A
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

#If A>>B, then ~A|B
def Material_Implication(expression1):
	if isinstance(expression1, conditional):
		return disjunction(negation(expression1[0]), expression1[1])
	elif isinstance(expression1, disjunction) and isinstance(expression1[0], negation):
		return conditional(expression1[0][0], expression1[1])
	return "INVALID OPERATION: Material Implication does not apply"

#If A**B, then (A>>B)&(A>>B) and (A&B)|(~A&~B)
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
#If (A&B)>>C, then A>>(B>>C)
def Exportation(expression1):
	if isinstance(expression1, conditional) and isinstance(expression1[0], conjunction):
		return conditional(expression1[0][0], conditional(expression1[0][1], expression1[1]))
	elif isinstance(expression1, conditional)  and isinstance(expression1[1], conditional):
		return conditional(conjunction(expression1[0], expression1[1].contents[0]), expression1[1][1])
	return "INVALID OPERATION: Exportation does not apply"

#If A, then A|A and A&A
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

