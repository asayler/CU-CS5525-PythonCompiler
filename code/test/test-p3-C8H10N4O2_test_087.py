#!/usr/bin/python

def f():
  x = 0
  y = 1
  def getx():
      return x
  def gety():
      return y
  f = getx if input() else gety
  x = 100
  return f

g = f()
print g()

h =f()
print h()
