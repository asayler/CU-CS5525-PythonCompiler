#!/usr/bin/python

# Andy Sayler
# Fall 2012
# CU CS5525
# Visitor functions for instruction selection
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

import sys

# Data Types
from compiler.ast import *
from monoast import *
from x86ast import *

# Helper Tools
from vis import Visitor

def arg_select(ast):
    if isinstance(ast, Name):
        return Var86(ast.name)
    elif isinstance(ast, Const):
        return Const86(ast.value)
    else:
        raise Exception("InstrSelect: Invalid argument - " + str(ast))

DISCARDTEMP = "discardtemp"
NULLTEMP = "nulltemp"
WORDLEN = 4

class InstrSelectVisitor(Visitor):

    # Modules

    def visitModule(self, n):
        return self.dispatch(n.node)

    # Statements    

    def visitStmt(self, n):
        instrs = []
        for s in n.nodes:
            instrs += self.dispatch(s)
        return instrs

    def visitAssign(self, n):
        return self.dispatch(n.expr, Var86(n.nodes[0].name))
        
    def visitDiscard(self, n):
        return self.dispatch(n.expr, Var86(DISCARDTEMP))
    
    # Terminal Expressions

    def visitConst(self, n, target):
        return [Move86(Const86(n.value), target)]

    def visitName(self, n, target):
        return [Move86(Var86(n.name), target)]

    # Non-Terminal Expressions

    def visitList(self, n):
        nodes = []
        for node in n.nodes:
            nodes += self.dispatch(node)
        return

    def visitDict(self, n):
        items = []
        for item in n.items:
            items += self.dispatch(item);
        return 

    def visitSubscript(self, n):
        return 
        
    def visitCompare(self, n):
        ops = []
        for op in n.ops:
            newop = (op[0], self.dispatch(op[1]))
            ops += [newop]
        return 

    def visitAdd(self, n, target):
        instrs = []
        instrs += [Move86(argselect(n.left), target)]
        instrs += [Add86(argselect(n.right), target)]
        return instrs
        
    def visitOr(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return 

    def visitAnd(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return 

    def visitNot(self, n):
        return 

    def visitUnarySub(self, n, target):
        instrs = []
        instrs += [Move86(arg_select(n.expr), target)]
        instrs += [Neg86(target)]
        return instrs

    def visitIfExp(self, n):
        return 

    def visitCallFunc(self, n, target):
        instrs = []
        cntargs = 0
        for arg in n.args:
            cntargs += 1
            instrs += [Push86(arg_select(arg))]
        instrs += [Call86(n.node.name)]
        instrs += [Move86(EAX, target)]
        if(cntargs > 0):
            instrs += [Add86(Const86(WORDLEN * cntargs), ESP)]
        return instrs