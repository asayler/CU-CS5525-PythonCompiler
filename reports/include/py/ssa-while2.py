x@0 = input()
x@2 = PHI(x@0, x@1)
while x@2 != 0:
    print x@2
    x@1 = x@2 - 1
print x@2
