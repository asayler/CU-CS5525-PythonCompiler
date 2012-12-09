#!/usr/bin/python


INC = [0]

def incr():
	INC[0] = INC[0] + 1
	return INC[0]


i = 0

dct = {incr():incr(), incr():incr()}

while i != 10:
	j = 0

	while j != 10:
		j = j + 1
		dct[incr()] = incr()

	i = i + 1

print dct[2]
print dct[4]
print dct[100]
print dct[102]
print dct[204]

y = 1
class A:
	x = 1
	def __init__(self, x):
		self.y = x + 2
	
	def foo(self):
		print y
		self.z = 6

	def bar(self):

		class D(A):
			z = 5

			def bar(self):
				self.z = self.z + 1

		return D


a = A(15)
a.foo()
print a.z

print A.x
print a.x

def foo():
	print 22

a.foo()

A.foo(a)

d = a.bar()

dd = d(30)

print dd.z

dd.bar()

print dd.z
print dd.y
print d.x
