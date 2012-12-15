# CU CS5525
# Fall 2012
# GSV Python Compiler
#
# analyze.py
# Script to Analyze Benchmark Results and Compute Speedup Ratios
#
# Repository:
#    https://github.com/asayler/CU-CS5525-PythonCompiler
#
# By :
#    Anne Gatchell
#       http://annegatchell.com/
#    Andrew (Andy) Sayler
#       http://www.andysayler.com
#    Michael (Mike) Vitousek
#       http://csel.cs.colorado.edu/~mivi2269/
#
# Copyright (c) 2012 by Anne Gatchell, Andy Sayler, and Mike Vitousek
#
# This file is part of the GSV CS5525 Fall 2012 Python Compiler.
#
#    The GSV CS5525 Fall 2012 Python Compiler is free software: you
#    can redistribute it and/or modify it under the terms of the GNU
#    General Public License as published by the Free Software
#    Foundation, either version 3 of the License, or (at your option)
#    any later version.
#
#    The GSV CS5525 Fall 2012 Python Compiler is distributed in the
#    hope that it will be useful, but WITHOUT ANY WARRANTY; without
#    even the implied warranty of MERCHANTABILITY or FITNESS FOR A
#    PARTICULAR PURPOSE.  See the GNU General Public License for more
#    details.
#
#    You should have received a copy of the GNU General Public License
#    along with the GSV CS5525 Fall 2012 Python Compiler.  If not, see
#    <http://www.gnu.org/licenses/>.

import os

def basename(f):
    return f[:f.rfind('.')]

testdir = 'bench'
llcruntimes = {}
lliruntimes = {}
llccmptimes = {}
llicmptimes = {}
x86runtimes = {}
x86cmptimes = {}
for (root, _, files) in os.walk(testdir):
    for f in files:
        f = os.path.join(root, f)
        if f.endswith('.llcrt'):
            llcruntimes[basename(f)] = open(f, 'r')
        elif f.endswith('.llirt'):
            lliruntimes[basename(f)] = open(f, 'r')        
        elif f.endswith('.llcct'):
            llccmptimes[basename(f)] = open(f, 'r')
        elif f.endswith('.llict'):
            llicmptimes[basename(f)] = open(f, 'r')
        elif f.endswith('.86rt'):
            x86runtimes[basename(f)] = open(f, 'r')
        elif f.endswith('.86ct'):
            x86cmptimes[basename(f)] = open(f, 'r')

total86cmp   = 0
totalllccmp  = 0
totalllicmp  = 0
total86run   = 0
totalllcrun  = 0
totalllirun  = 0

for name in llcruntimes:
    if not (name in llccmptimes and name in x86runtimes and name in x86cmptimes):
        continue
    llct = float(llccmptimes[name].readline().rstrip())
    x86ct = float(x86cmptimes[name].readline().rstrip())
    cratio = -1 if x86ct == 0 else (llct / x86ct)

    print '%s compile time ratio: %fx (%fs / %fs)' % (name, 1/cratio, llct, x86ct)

    llrt = float(llcruntimes[name].readline().rstrip())
    x86rt = float(x86runtimes[name].readline().rstrip())
    rratio = -1 if x86rt == 0 else (llrt / x86rt)
    
    print '%s runtime ratio: %fx (%fs / %fs)' % (name, 1/rratio, llrt, x86rt)

    total86cmp  += x86ct
    totalllccmp += llct
    total86run  += x86rt
    totalllcrun += llrt

cratio = -1 if total86cmp == 0 else (totalllccmp / total86cmp)
rratio = -1 if total86run == 0 else (totalllcrun / total86run)

print 'Overall compile time ratio: %fx' % (1/cratio)
print 'Overall runtime ratio: %fx' % (1/rratio)
print '(Negative numbers indicate division by zero)'
