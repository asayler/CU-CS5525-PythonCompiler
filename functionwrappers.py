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
def CallISINT(args):
    return CallFunc(ISINT_n, args)

def CallISBOOL(args):
    return CallFunc(ISBOOL_n, args)

def CallISBIG(args):
    return CallFunc(ISBIG_n, args)

# Inject Macros
def CallINJECTINT(args):
    return CallFunc(INJECTINT_n, args)

def CallINJECTBOOL(args):
    return CallFunc(INJECTBOOL_n, args)

def CallINJECTBIG(args):
    return CallFunc(INJECTBIG_n, args)

# Project Macros
def CallPROJECTINT(args):
    return CallFunc(PROJECTINT_n, args)

def CallPROJECTBOOL(args):
    return CallFunc(PROJECTBOOL_n, args)

def CallPROJECTBIG(args):
    return CallFunc(PROJECTBIG_n, args)

# Utility Macros
def CallBIGADD(args):
    return CallFunc(BIGADD_n, args)

def CallTERROR(args):
    return CallFunc(TERROR_n, args)

def CallPRINTANY(args):
    return CallFunc(PRINTANY_n, args)
