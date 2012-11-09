#!/usr/bin/python

class c():
 def f(self, x):
  self.x = x

class v():
 def f(self, x):
  self.x = x

x = input()
C = c()
C.f(x)

V = v()
V.f(x)

print V.x
print C.x
