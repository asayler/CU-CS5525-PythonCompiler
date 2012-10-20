# CU CS5525
# Fall 2012
# Python Compiler
#
# monoast.py
# Monomorphic (explicit) Intermediate AST Nodes
# Reg Alloc Module
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

class PyType(object):
    """Class to represent type constants"""
    def __init__(self, typ):
        self.typ = typ
    def __repr__(self):
        return "MONOTYPE(%s)" % (self.typ)
    def __hash__(self):
        return hash(self.__repr__())
    def __eq__(self, that):
        return self.__repr__() == repr(that)

INT_t      = PyType('INT')
BOOL_t     = PyType('BOOL')
BIG_t      = PyType('BIGPYOBJ')

class PyNode(object):
    """Abstaract base class for monoast nodes"""
    def __str__(self):
        return repr(self)

# New Mono Nodes

class SLambda(PyNode):
    def __init__(self, params, code):
        self.params = params
        self.code = code

    def __repr__(self):
        return 'SLambda(%s, %s)' % (self.params, self.code) 
    @staticmethod
    def visitSLambda(self, n):
        return SLambda(map(self.dispatch, n.params), self.dispatch(n.code))

class IndirectCallFunc(PyNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args
    def __repr__(self):
        return 'IndirectCallFunc(%s, %s)' % (self.name, self.args)
    @staticmethod
    def visitIndirectCallFunc(self, n):
        return IndirectCallFunc(self.dispatch(n.name), map(self.dispatch, n.args))

class InstrSeq(PyNode):
    def __init__(self, nodes, expr):
        self.nodes = nodes
        self.expr = expr
    def __repr__(self):
        return "InstrSeq(%s, %s)" % (repr(self.nodes), repr(self.expr))
    @staticmethod
    def visitInstrSeq(self, n):
        return InstrSeq(map(self.dispatch, nodes), self.dispatch(n.expr))

class IsTag(PyNode):
    """Call code to determine if 'arg' is of type 'typ'"""
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
    def __repr__(self):
        return "IsTag(%s, %s)" % (repr(self.typ), repr(self.arg))
    @staticmethod
    def visitIsTag(self, n):
        return IsTag(self.dispatch(n.typ), self.dispatch(n.arg))

class InjectFrom(PyNode):
    """Convert result of 'arg' from 'typ' to pyobj"""
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
    def __repr__(self):
        return "InjectFrom(%s, %s)" % (repr(self.typ), repr(self.arg))
    @staticmethod
    def visitInjectFrom(self, n):
        return InjectFrom(self.dispatch(n.typ), self.dispatch(n.arg))

class ProjectTo(PyNode):
    """Convert result of 'arg' from pyobj to 'typ'"""
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
    def __repr__(self):
        return "ProjectTo(%s, %s)" % (repr(self.typ), repr(self.arg))
    @staticmethod
    def visitProjectTo(self, n):
        return ProjectTo(self.dispatch(n.typ), self.dispatch(n.arg))

class Let(PyNode):
    """Evaluate 'var' = 'rhs', than run body referencing 'var'"""
    def __init__(self, var, rhs, body):
        self.var  = var
        self.rhs  = rhs
        self.body = body
    def __repr__(self):
        return "Let(%s, %s, %s)" % (repr(self.var), repr(self.rhs), repr(self.body))
    @staticmethod
    def visitLet(self, n):
        return Let(self.dispatch(n.var), self.dispatch(n.rhs), self.dispatch(n.body))

# General AST Nodes
class SubscriptAssign:
    '''Assignment statement for subscription'''
    def __init__(self, target, sub, value):
        self.target = target
        self.sub = sub
        self.value = value

    def __repr__(self):
        return "SubscriptAssign(%s, %s, %s)" % (repr(self.target), repr(self.sub), repr(self.value))

    @staticmethod
    def visitSubscriptAssign(self, n):
        return SubscriptAssign(self.dispatch(n.target), self.dispatch(n.sub), self.dispatch(n.value))

class IntEqual(PyNode):
    def __init__(self, (left, right), lineno=None):
        self.left = left
        self.right = right
        self.lineno = lineno

    def __repr__(self):
        return "IntEqual(%s, %s)" % (repr(self.left), repr(self.right))

    @staticmethod
    def visitIntEqual(self, n):
        return IntEqual((self.dispatch(n.left), self.dispatch(n.right)), n.lineno)

class IntNotEqual(PyNode):
    def __init__(self, (left, right), lineno=None):
        self.left = left
        self.right = right
        self.lineno = lineno

    def __repr__(self):
        return "IntNotEqual(%s, %s)" % (repr(self.left), repr(self.right))

    @staticmethod
    def visitIntNotEqual(self, n):
        return IntNotEqual((self.dispatch(n.left), self.dispatch(n.right)), n.lineno)

class IntAdd(PyNode):
    def __init__(self, (left, right), lineno=None):
        self.left = left
        self.right = right
        self.lineno = lineno

    def __repr__(self):
        return "IntAdd((%s, %s))" % (repr(self.left), repr(self.right))

    @staticmethod
    def visitIntAdd(self, n):
        return IntAdd((self.dispatch(n.left), self.dispatch(n.right)), n.lineno)

class IntUnarySub(PyNode):
    def __init__(self, expr, lineno=None):
        self.expr = expr
        self.lineno = lineno

    def __repr__(self):
        return "IntUnarySub(%s)" % (repr(self.expr))

    @staticmethod
    def visitIntUnarySub(self, n):
        return IntUnarySub(self.dispatch(n.expr), n.lineno)
