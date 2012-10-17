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
BIG_t      = mono_Type('BIGPYOBJ')

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

class mono_IfExp(mono_Node):
    """Evaluate if exp with explicated test"""
    def __init__(self, test, then, else_):
        self.test = test
        self.then = then
        self.else_ = else_
    def __repr__(self):
        return "mono_IfExp(%s, %s, %s)" % (repr(self.test), repr(self.then), repr(self.else_))

# General AST Nodes

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

class mono_IntEqual(mono_Node):
    def __init__(self, (left, right), lineno=None):
        self.left = left
        self.right = right
        self.lineno = lineno

    def __repr__(self):
        return "mono_IntEqual(%s, %s)" % (repr(self.left), repr(self.right))

class mono_IntNotEqual(mono_Node):
    def __init__(self, (left, right), lineno=None):
        self.left = left
        self.right = right
        self.lineno = lineno

    def __repr__(self):
        return "mono_IntNotEqual(%s, %s)" % (repr(self.left), repr(self.right))

class mono_IntAdd(mono_Node):
    def __init__(self, (left, right), lineno=None):
        self.left = left
        self.right = right
        self.lineno = lineno

    def __repr__(self):
        return "mono_IntAdd((%s, %s))" % (repr(self.left), repr(self.right))

class mono_IntUnarySub(mono_Node):
    def __init__(self, expr, lineno=None):
        self.expr = expr
        self.lineno = lineno

    def __repr__(self):
        return "mono_IntUnarySub(%s)" % (repr(self.expr))
