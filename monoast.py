# Andy Sayler
# Fall 2012
# CU CS5525
# Python Compiler
# Monomorphic (explicit) Intermediate AST Nodes
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

from compiler.ast import *

class mono_Type:
    """Class to represent type constants"""
    def __init__(self, typ):
        self.typ = typ
    def __repr__(self):
        return "MONOTYPE(%s)" % (self.typ)
    def __hash__(self):
        return hash(self.__repr__())
    def __eq__(self, that):
        return self.__repr__() == repr(that)

INT_t      = mono_Type('INT')
BOOL_t     = mono_Type('BOOL')
BIGPYOBJ_t = mono_Type('BIGPYOBJ')

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

def CallISINT(var):
    return CallFunc(ISINT_n, var)

def CallISBOOL(var):
    return CallFunc(ISBOOL_n, var)

def CallISBIG(var):
    return CallFunc(ISBIG_n, var)


def CallINJECTINT(var):
    return CallFunc(INJECTINT_n, var)

def CallINJECTBOOL(var):
    return CallFunc(INJECTBOOL_n, var)

def CallINJECTBIG(var):
    return CallFunc(INJECTBIG_n, var)


def CallPROJECTINT(var):
    return CallFunc(PROJECTINT_n, var)

def CallPROJECTBOOL(var):
    return CallFunc(PROJECTBOOL_n, var)

def CallPROJECTBIG(var):
    return CallFunc(PROJECTBIG_n, var)



class mono_Node:
    """Abstaract base class for monoast nodes"""
    # Do nothing, just a placeholder in case we want to add to it later

# New Mono Nodes

class mono_IsTag(mono_Node):
    """Call code to determine if 'arg' is of type 'typ'"""
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
    def __repr__(self):
        return "mono_IsTag(%s, %s)" % (repr(self.typ), repr(self.arg))

class mono_InjectFrom(mono_Node):
    """Convert result of 'arg' from 'typ' to pyobj"""
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
    def __repr__(self):
        return "mono_InjectFrom(%s, %s)" % (repr(self.typ), repr(self.arg))

class mono_ProjectTo(mono_Node):
    """Convert result of 'arg' from pyobj to 'typ'"""
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
    def __repr__(self):
        return "mono_ProjectTo(%s, %s)" % (repr(self.typ), repr(self.arg))

class mono_Let(mono_Node):
    """Evaluate 'var' = 'rhs', than run body referencing 'var'"""
    def __init__(self, var, rhs, body):
        self.var  = var
        self.rhs  = rhs
        self.body = body
    def __repr__(self):
        return "mono_Let(%s, %s, %s)" % (repr(self.var), repr(self.rhs), repr(self.body))

# General AST Nodes

class mono_Printnl(mono_Node):
    def __init__(self, nodes, dest, lineno=None):
        self.nodes = nodes
        self.dest = dest
        self.lineno = lineno

    def __repr__(self):
        return "mono_Printnl(%s, %s)" % (repr(self.nodes), repr(self.dest))

class mono_Assign(mono_Node):
    def __init__(self, nodes, expr, lineno=None):
        self.nodes = nodes
        self.expr = expr
        self.lineno = lineno

    def __repr__(self):
        return "mono_Assign(%s, %s)" % (repr(self.nodes), repr(self.expr))

class mono_Const(mono_Node):
    def __init__(self, value, lineno=None):
        self.value = value
        self.lineno = lineno

    def __repr__(self):
        return "mono_Const(%s)" % (repr(self.value))

class mono_List(mono_Node):
    def __init__(self, nodes, lineno=None):
        self.nodes = nodes
        self.lineno = lineno

    def __repr__(self):
        return "mono_List(%s)" % (repr(self.nodes))

class mono_Dict(mono_Node):
    def __init__(self, items, lineno=None):
        self.items = items
        self.lineno = lineno

    def __repr__(self):
        return "mono_Dict(%s)" % (repr(self.items))

class mono_Subscript(mono_Node):
    def __init__(self, expr, flags, subs, lineno=None):
        self.expr = expr
        self.flags = flags
        self.subs = subs
        self.lineno = lineno

    def __repr__(self):
        return "mono_Subscript(%s, %s, %s)" % (repr(self.expr), repr(self.flags), repr(self.subs))

class mono_Compare(mono_Node):
    def __init__(self, expr, ops, lineno=None):
        self.expr = expr
        self.ops = ops
        self.lineno = lineno

    def __repr__(self):
        return "mono_Compare(%s, %s)" % (repr(self.expr), repr(self.ops))

class mono_IntAdd(mono_Node):
    def __init__(self, (left, right), lineno=None):
        self.left = left
        self.right = right
        self.lineno = lineno

    def __repr__(self):
        return "mono_IntAdd((%s, %s))" % (repr(self.left), repr(self.right))

class mono_UnarySub(mono_Node):
    def __init__(self, expr, lineno=None):
        self.expr = expr
        self.lineno = lineno

    def __repr__(self):
        return "mono_UnarySub(%s)" % (repr(self.expr))
