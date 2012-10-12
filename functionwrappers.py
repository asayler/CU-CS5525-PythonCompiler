# Andy Sayler
# Fall 2012
# CU CS5525
# Python Compiler
# Function Wrappers for Helper Functions
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

from compiler.ast import *
from x86ast import *

# Function Names

ISINT_n    = Name("is_int")
ISBOOL_n   = Name("is_bool")
ISBIG_n    = Name("is_big")

INJECTINT_n  = Name("inject_int")
INJECTBOOL_n = Name("inject_bool")
INJECTBIG_n  = Name("inject_big")

PROJECTINT_n  = Name("project_int")
PROJECTBOOL_n = Name("project_bool")
PROJECTBIG_n  = Name("project_big")

BIGADD_n   = Name("add")
TERROR_n   = Name("error_pyobj")
PRINTANY_n = Name("print_any")



# Function Wrappers

# Is Macros
def CallISINT(arg):
    return CallFunc(ISINT_n, [arg])

def CallISBOOL(arg):
    return CallFunc(ISBOOL_n, [arg])

def CallISBIG(arg):
    return CallFunc(ISBIG_n, [arg])

# Inject Macros
def CallINJECTINT(arg):
    return CallFunc(INJECTINT_n, [arg])

def CallINJECTBOOL(arg):
    return CallFunc(INJECTBOOL_n, [arg])

def CallINJECTBIG(arg):
    return CallFunc(INJECTBIG_n, [arg])

# Project Macros
def CallPROJECTINT(arg):
    return CallFunc(PROJECTINT_n, [arg])

def CallPROJECTBOOL(arg):
    return CallFunc(PROJECTBOOL_n, [arg])

def CallPROJECTBIG(arg):
    return CallFunc(PROJECTBIG_n, [arg])

# Utility Macros
def CallBIGADD(arg):
    return CallFunc(BIGADD_n, [arg])

def CallTERROR(arg):
    return CallFunc(TERROR_n, [arg])
