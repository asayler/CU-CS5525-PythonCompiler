# CU CS5525
# Fall 2012
# Python Compiler
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
#    Andy Sayler
#       http://www.andysayler.com
#    Michael (Mike) Vitousek
#       http://csel.cs.colorado.edu/~mivi2269/

from pyast import *

SEPERATOR    = '_'
LABEL_PREFIX = 'l'
RETURNL      = "return"
ELSEL        = "else"
ENDIFL       = "endelse"
WHILESTARTL  = "whilestart"
WHILEENDL    = "whileend"

counter = 1

def generte_cnt_str():
    global counter
    name = str(counter)
    counter += 1
    return name

def generate_name(x):
    name = generte_cnt_str() + SEPERATOR + x
    return name

def generate_return_label(funcName):
    return LABEL_PREFIX + SEPERATOR + str(funcName) + SEPERATOR + RETURNL

def generate_while_labels():
    cntStr = generte_cnt_str()
    startLStr = LABEL_PREFIX + SEPERATOR + WHILESTARTL + SEPERATOR + cntStr
    endLStr   = LABEL_PREFIX + SEPERATOR + WHILEENDL   + SEPERATOR + cntStr
    return (startLStr, endLStr)

def generate_if_labels(length):
    cntStr = generte_cnt_str()
    caseLStr = []
    for i in xrange(0, length):
        caseLStr += [LABEL_PREFIX + SEPERATOR + ELSEL + SEPERATOR + str(i) + SEPERATOR + cntStr]
    endLStr  = LABEL_PREFIX + SEPERATOR + ENDIFL + SEPERATOR + cntStr
    return (caseLStr, endLStr)

def make_assign(lhs, rhs):
    return VarAssign(lhs, rhs)
