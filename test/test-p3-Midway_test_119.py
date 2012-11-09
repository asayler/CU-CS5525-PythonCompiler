#!/usr/bin/python

class C():
	x = 1
	def f(x):
		return 2+x
print C.f(2)
print C.f(C.x)
