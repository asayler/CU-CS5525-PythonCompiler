# CU CS5525
# Fall 2012
# Python Compiler
#
# explicate.py
# Visitor Functions to Explicate AST
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

import sys

# Data Types
from compiler.ast import *
from monoast import *

from unitcopy import CopyVisitor

# Helper Types
from vis import Visitor
from functionwrappers import *
from utilities import generate_name

#Reserved Names
TRUENAME   = "True"
TRUEVALUE  = 1
FALSENAME  = "False"
FALSEVALUE = 0
TRUENODE   = InjectFrom(BOOL_t, Const(TRUEVALUE))
FALSENODE  = InjectFrom(BOOL_t, Const(FALSEVALUE))

COMPEQUAL    = '=='
COMPNOTEQUAL = '!='
COMPIS       = 'is'

class AssignSpecializeVisitor(CopyVisitor):
    def visitAssign(self, n):
        # Separate out variable assignment from subscript assignment?
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        # Only worrying about first assignee
        if isinstance(nodes[0], Subscript):
            return SubscriptAssign(nodes[0].expr,
                                   nodes[0].subs[0],
                                   self.dispatch(n.expr))
        elif isinstance(nodes[0], AssAttr):
            return AttrAssign(nodes[0].expr,
                               nodes[0].attrname.
                               self.dispatch(n.expr))
        else:
            return Assign(nodes, self.dispatch(n.expr), n.lineno)
