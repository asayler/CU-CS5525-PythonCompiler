def x(a):
	def x(b, c):
		return b+c
	return(x(a,1))

print x(3)