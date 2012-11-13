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

# For modules after closure conversion
def visitModulePostCC(self, n):
    return Module(n.doc, map(self.dispatch, n.node), n.lineno) 

class PyNode(object):
    """Abstaract base class for monoast nodes"""
    def __str__(self):
        return repr(self)

class SLambda(PyNode):
    def __init__(self, params, code, label=None):
        self.params = params
        self.code = code
        self.label = label        

    def __repr__(self):
        return 'SLambda(%s, %s, %s)' % (self.params, self.code, self.label) 
    @staticmethod
    def visitSLambda(self, n):
        return SLambda(n.params, self.dispatch(n.code), n.label)

class SLambdaLabel(PyNode):
    def __init__(self, name):
        self.name = name
                
    def __repr__(self):
        return 'SLambdaLabel(%s)' % (self.name) 
    @staticmethod
    def visitSLambdaLabel(self, n):
        return SLambdaLabel(n.name)

class IndirectCallFunc(PyNode):
    def __init__(self, node, args):
        self.node = node
        self.args = args
    def __repr__(self):
        return 'IndirectCallFunc(%s, %s)' % (self.node, self.args)
    @staticmethod
    def visitIndirectCallFunc(self, n):
        return IndirectCallFunc(self.dispatch(n.node), map(self.dispatch, n.args))

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
        return IsTag(n.typ, self.dispatch(n.arg))

class InjectFrom(PyNode):
    """Convert result of 'arg' from 'typ' to pyobj"""
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
    def __repr__(self):
        return "InjectFrom(%s, %s)" % (repr(self.typ), repr(self.arg))
    @staticmethod
    def visitInjectFrom(self, n):
        return InjectFrom(n.typ, self.dispatch(n.arg))

class ProjectTo(PyNode):
    """Convert result of 'arg' from pyobj to 'typ'"""
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
    def __repr__(self):
        return "ProjectTo(%s, %s)" % (repr(self.typ), repr(self.arg))
    @staticmethod
    def visitProjectTo(self, n):
        return ProjectTo(n.typ, self.dispatch(n.arg))

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

class AttrAssign:
    '''Assignment statement for attributes'''
    def __init__(self, target, attr, value):
        self.target = target
        self.attr = attr
        self.value = value

    def __repr__(self):
        return "AttrAssign(%s, %s, %s)" % (repr(self.target), repr(self.attr), repr(self.value))

    @staticmethod
    def visitAttrAssign(self, n):
        return AttrAssign(self.dispatch(n.target), n.attr, self.dispatch(n.value))


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

class WhileFlat(PyNode):
    def __init__(self, testss, test, body, else_, lineno=None):
        self.testss = testss
        self.test = test
        self.body = body
        self.else_ = else_
        self.lineno = lineno

    def __repr__(self):
        return "WhileFlat(%s ,%s, %s, %s)" % (repr(self.testss), repr(self.test),
                                              repr(self.body), repr(self.else_))
    @staticmethod
    def visitWhilePostCC(self, n):
        return WhilePostCC(self.dispatch(n.testss),
                           self.dispatch(n.test),
                           self.dispatch(n.body),
                           n.else_,
                           n.lineno)

class String(PyNode):
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return 'String(%s)' % self.string
