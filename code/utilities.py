# CU CS5525
# Fall 2012
# GSV Python Compiler
#
# utilities.py
# Compiler Utility Functions
#
# Adopted from code by Jeremy Siek, Fall 2012
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

from pyast import *

SEPERATOR    = '_'
NAME_PREFIX  = 'n'
LABEL_PREFIX = 'l'
RETURNL      = "return"
ELSEL        = "else"
ENDIFL       = "endelse"
WHILESTARTL  = "whilestart"
WHILEENDL    = "whileend"

counter = 1

def generate_cnt_str():
    global counter
    name = str(counter)
    counter += 1
    return name

def generate_name(x):
    name = NAME_PREFIX + SEPERATOR + generate_cnt_str() + SEPERATOR + x
    return name

def generate_label(x):
    return LABEL_PREFIX + SEPERATOR + generate_cnt_str()+ SEPERATOR + x

def generate_return_label(funcName):
    return LABEL_PREFIX + SEPERATOR + str(funcName) + SEPERATOR + RETURNL

def generate_while_labels():
    cntStr = generate_cnt_str()
    startLStr = LABEL_PREFIX + SEPERATOR + WHILESTARTL + SEPERATOR + cntStr
    endLStr   = LABEL_PREFIX + SEPERATOR + WHILEENDL   + SEPERATOR + cntStr
    return (startLStr, endLStr)

def generate_if_labels(length):
    cntStr = generate_cnt_str()
    caseLStr = []
    for i in xrange(0, length):
        caseLStr += [LABEL_PREFIX + SEPERATOR + ELSEL + SEPERATOR + str(i) + SEPERATOR + cntStr]
    endLStr  = LABEL_PREFIX + SEPERATOR + ENDIFL + SEPERATOR + cntStr
    return (caseLStr, endLStr)

def make_assign(lhs, rhs):
    return VarAssign(lhs, rhs)
