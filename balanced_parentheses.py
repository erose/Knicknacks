"""
Converts strings of balanced parentheses to LISP-style number lists.

(()()) --> (1, 1)
((()()())(())) --> ((1, 1, 1), 2)
"""

def f(stack):
	if stack[-1] == "(":
		return 0

	tup = ()
	for entry in reversed(stack):

		if entry == "(":
			if len(tup) == 1: return tup[0] + 1
			else: return tup
		else:
			tup = (entry,) + tup

		stack.pop()

def parens_to_LISP(paren_string):
	stack = []

	for p in paren_string:
		if p == "(":
			stack.append(p)

		if p == ")":
			stack[-1] = f(stack)

	return stack[0]

if __name__ == "__main__":
	import sys
	print(parens_to_LISP(sys.argv[1]))
