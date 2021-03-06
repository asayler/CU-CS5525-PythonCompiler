# CU CS5525
# Fall 2012
# GSV Python Compiler
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
GERROR_n   = Name("error_general")
BERROR_n   = Name("error_binary")
PRINTANY_n = Name("print_any")
ISTRUE_n   = Name("is_true")

MAKELIST_n = Name("create_list")
MAKEDICT_n = Name("create_dict")
SETSUB_n   = Name("set_subscript")
GETSUB_n   = Name("get_subscript")

CREATECLOSURE_n = Name("create_closure")
GETFUNPTR_n = Name("get_fun_ptr")
GETFREEVARS_n = Name("get_free_vars")

CREATECLASS_n = Name('create_class')
CREATEOBJECT_n = Name('create_object')
HASATTR_n = Name('has_attr')
GETFUNCTION_n = Name('get_function')
GETRECEIVER_n = Name('get_receiver')
ISBOUNDMETHOD_n = Name('is_bound_method')
ISUNBOUNDMETHOD_n = Name('is_unbound_method')
ISCLASS_n = Name('is_class')
SETATTR_n = Name('set_attr')
GETATTR_n = Name('get_attr')

RESERVED_NAMES = [
    ISINT_n.name,
    ISBOOL_n.name,
    ISBIG_n.name,
    INJECTINT_n.name,
    INJECTBOOL_n.name,
    INJECTBIG_n.name,
    PROJECTINT_n.name,
    PROJECTBOOL_n.name,
    PROJECTBIG_n.name,
    BIGADD_n.name,
    BIGEQ_n.name,
    BIGNEQ_n.name,
    TERROR_n.name,
    GERROR_n.name,
    BERROR_n.name,
    PRINTANY_n.name,
    ISTRUE_n.name,
    MAKELIST_n.name,
    MAKEDICT_n.name,
    SETSUB_n.name,
    GETSUB_n.name,
    CREATECLOSURE_n.name,
    GETFUNPTR_n.name,
    GETFREEVARS_n.name,
    CREATECLASS_n.name,
    CREATEOBJECT_n.name,
    HASATTR_n.name,
    GETFUNCTION_n.name,
    GETRECEIVER_n.name,
    ISBOUNDMETHOD_n.name,
    ISUNBOUNDMETHOD_n.name,
    ISCLASS_n.name,
    SETATTR_n.name,
    GETATTR_n.name,
    'input',
    'input_int',
    'True',
    'False'
    ]

# Class macros

def CallCREATECLASS(args):
    return CallFunc(CREATECLASS_n, args)

def CallCREATEOBJECT(args):
    return CallFunc(CREATEOBJECT_n, args)

def CallHASATTR(args):
    return CallFunc(HASATTR_n, args)

def CallGETFUNCTION(args):
    return CallFunc(GETFUNCTION_n, args)

def CallGETRECEIVER(args):
    return CallFunc(GETRECEIVER_n, args)

def CallISBOUNDMETHOD(args):
    return CallFunc(ISBOUNDMETHOD_n, args)

def CallISUNBOUNDMETHOD(args):
    return CallFunc(ISUNBOUNDMETHOD_n, args)

def CallISCLASS(args):
    return CallFunc(ISCLASS_n, args)

def CallSETATTR(args):
    return CallFunc(SETATTR_n, args)

def CallGETATTR(args):
    return CallFunc(GETATTR_n, args)

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

# Operation Macros
def CallBIGADD(args):
    return CallFunc(BIGADD_n, args)

def CallBIGEQ(args):
    return CallFunc(BIGEQ_n, args)

def CallBIGNEQ(args):
    return CallFunc(BIGNEQ_n, args)

def CallBIGGT(args):
    return CallFunc(BERROR_n, args)

def CallBIGGE(args):
    return CallFunc(BERROR_n, args)

def CallBIGLT(args):
    return CallFunc(BERROR_n, args)

def CallBIGLE(args):
    return CallFunc(BERROR_n, args)

# Utility Macros
def CallTERROR(args):
    return CallFunc(TERROR_n, args)

def CallGERROR(args):
    return CallFunc(GERROR_n, args)

def CallBERROR(args):
    return CallFunc(BERROR_n, args)

def CallPRINTANY(args):
    return CallFunc(PRINTANY_n, args)

def CallISTRUE(args):
    return CallFunc(ISTRUE_n, args)

# List/Dict Macros
def CallMAKELIST(args):
    return CallFunc(MAKELIST_n, args)

def CallMAKEDICT(args):
    return CallFunc(MAKEDICT_n, args)

def CallSETSUB(args):
    return CallFunc(SETSUB_n, args)

def CallGETSUB(args):
    return CallFunc(GETSUB_n, args)

# Closure Macros
def CallCREATECLOSURE(args):
    return CallFunc(CREATECLOSURE_n, args)

def CallGETFUNPTR(args):
    return CallFunc(GETFUNPTR_n, args)

def CallGETFREEVARS(args):
    return CallFunc(GETFREEVARS_n, args)
