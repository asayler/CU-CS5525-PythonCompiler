#!/usr/bin/python

class C:
	x = 1
	def f(x):
		class D:
			x = 2
		print D.x
		print x
	print x
print C.x
print C.f(3)
