# CU CS5525
# Fall 2012
# Python Compiler
#
# functionwrappers.py
# Macro wrappers for helper functions
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
BIGEQ_n    = Name("equal")
BIGNEQ_n   = Name("not_equal")
TERROR_n   = Name("error_pyobj")
PRINTANY_n = Name("print_any")
ISTRUE_n   = Name("is_true")

MAKELIST_n = Name("create_list")
MAKEDICT_n = Name("create_dict")
SETSUB_n   = Name("set_subscript")
GETSUB_n   = Name("get_subscript")

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

def CallBIGEQ(args):
    return CallFunc(BIGEQ_n, args)

def CallBIGNEQ(args):
    return CallFunc(BIGNEQ_n, args)

def CallTERROR(args):
    return CallFunc(TERROR_n, args)

def CallPRINTANY(args):
    return CallFunc(PRINTANY_n, args)

def CallISTRUE(args):
    return CallFunc(ISTRUE_n, args)

#List/Dict Macros

def CallMAKELIST(args):
    return CallFunc(MAKELIST_n, args)

def CallMAKEDICT(args):
    return CallFunc(MAKEDICT_n, args)

def CallSETSUB(args):
    return CallFunc(SETSUB_n, args)

def CallGETSUB(args):
    return CallFunc(GETSUB_n, args)
