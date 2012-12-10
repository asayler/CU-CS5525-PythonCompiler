import os

def basename(f):
    return f[:f.rfind('.')]

testdir = 'build'
llruntimes = {}
llcmptimes = {}
x86runtimes = {}
x86cmptimes = {}
for (root, _, files) in os.walk(testdir):
    for f in files:
        f = os.path.join(root, f)
        if f.endswith('.llrt'):
            llruntimes[basename(f)] = open(f, 'r')
        elif f.endswith('.llct'):
            llcmptimes[basename(f)] = open(f, 'r')
        elif f.endswith('.86rt'):
            x86runtimes[basename(f)] = open(f, 'r')
        elif f.endswith('.86ct'):
            x86cmptimes[basename(f)] = open(f, 'r')

total86cmp = 0
totalllcmp = 0
total86run = 0
totalllrun = 0

for name in llruntimes:
    if not (name in llcmptimes and name in x86runtimes and name in x86cmptimes):
        continue
    llct = float(llcmptimes[name].readline().rstrip())
    x86ct = float(x86cmptimes[name].readline().rstrip())
    cratio = -1 if x86ct == 0 else (llct / x86ct)

    print '%s compile time ratio: %fx (%fs / %fs)' % (name, 1/cratio, llct, x86ct)

    llrt = float(llruntimes[name].readline().rstrip())
    x86rt = float(x86runtimes[name].readline().rstrip())
    rratio = -1 if x86rt == 0 else (llrt / x86rt)
    
    print '%s runtime ratio: %fx (%fs / %fs)' % (name, 1/rratio, llrt, x86rt)

    total86cmp += x86ct
    totalllcmp += llct
    total86run += x86rt
    totalllrun += llrt

cratio = -1 if total86cmp == 0 else (totalllcmp / total86cmp)
rratio = -1 if total86run == 0 else (totalllrun / total86run)

print 'Overall compile time ratio: %fx' % (1/cratio)
print 'Overall runtime ratio: %fx' % (1/rratio)
print '(Negative numbers indicate division by zero)'
