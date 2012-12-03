if input():
    x@0 = 42
else:
    if input():
        x@1 = True
    else:
        x@2 = [4,2]
    x@3 = PHI(x@1,x@2)
x@4 = PHI(x@0, x@3)
print x@4
