x@0 = input()
loop:
    x@2 = PHI(x@0, x@1)
    if x@2 != 0 goto start else goto end
start:
    print x@2
    x@1 = x@2 - 1
    goto loop
end:
    print x@2
