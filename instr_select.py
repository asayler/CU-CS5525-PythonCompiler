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
from flatast import *
from x86ast import *

# Helper Tools
from vis import Visitor
from utilities import generate_name

def arg_select(ast):
    if isinstance(ast, Name):
        return Var86(ast.name)
    elif isinstance(ast, Const):
        return Const86(ast.value)
    else:
        raise Exception("InstrSelect: Invalid argument - " + str(ast))

DISCARDTEMP = "discardtemp"
NULLTEMP = "nulltemp"
IFTEMP = "iftemp"

IfThenLabelCnt = 0
ELSELABEL  = "else"
ENDIFLABEL = "endelse"

class InstrSelectVisitor(Visitor):

    # Banned Nodes

    def visitAdd(self, n):
        raise Exception("'Add' node no longer valid at this stage")

    def visitUnarySub(self, n):
        raise Exception("'UnarySub' node no longer valid at this stage")

    def visitNot(self, n):
        raise Exception("'Not' node no longer valid at this stage")

    def visitCompare(self, n):
        raise Exception("'Compare' node no longer valid at this stage")

    def visitPrintnl(self, n):
        raise Exception("'Printnl' node no longer valid at this stage")

    def visitmono_IsTag(self, n):
        raise Exception("'mono_IsTag' node no longer valid at this stage")

    def visitmono_ProjectTo(self, n):
        raise Exception("'mono_ProjectTo' node no longer valid at this stage")

    def visitmono_InjectFrom(self, n):
        raise Exception("'mono_InjectFrom' node no longer valid at this stage")

    def visitAnd(self, n):
        raise Exception("'And' node no longer valid at this stage")

    def visitOr(self, n):
        raise Exception("'Or' node no longer valid at this stage")

    def visitmono_Let(self, n):
        raise Exception("'Let' node no longer valid at this stage")

    def mono_IsTrue(self, n):
        raise Exception("'mono_IsTrue' node no longer valid at this stage")

    def IfExp(self, n):
        raise Exception("'IfExp' node no longer valid at this stage")

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
        tmp = Var86(generate_name(DISCARDTEMP))
        return self.dispatch(n.expr, tmp)
    
    # Terminal Expressions

    def visitConst(self, n, target):
        return [Move86(Const86(n.value), target)]

    def visitName(self, n, target):
        return [Move86(Var86(n.name), target)]

    # Non-Terminal Expressions

    def visitmono_IntAdd(self, n, target):
        instrs = []
        instrs += [Move86(arg_select(n.left), target)]
        instrs += [Add86(arg_select(n.right), target)]
        return instrs

    def visitmono_IntEqual(self, n, target):
        instrs = []
        instrs += [Move86(arg_select(n.left), target)]
        instrs += [Comp86(arg_select(n.right), target)]
        # prezero register (avoids call to movebzl)
        instrs += [Move86(x86ZERO, target)]
        instrs += [SetEq86(target)]
        return instrs

    def visitmono_IntNotEqual(self, n, target):
        instrs = []
        instrs += [Move86(arg_select(n.left), target)]
        instrs += [Comp86(arg_select(n.right), target)]
        # prezero register (avoids call to movebzl)
        instrs += [Move86(x86ZERO, target)]
        instrs += [SetNEq86(target)]
        return instrs

    def visitmono_IntUnarySub(self, n, target):
        instrs = []
        instrs += [Move86(arg_select(n.expr), target)]
        instrs += [Neg86(target)]
        return instrs

    def visitmono_IfExp(self, n, target):
        #Setup Label
        global IfThenLabelCnt
        ElseLStr  = ELSELABEL + str(IfThenLabelCnt)
        EndIfLStr = ENDIFLABEL + str(IfThenLabelCnt)
        IfThenLabelCnt += 1
        # Test Instructions
        test  = []
        test += self.dispatch(n.test, target)
        test += [Comp86(x86FALSE, target)]
        test += [JumpEqual86(ElseLStr)]
        # Then Instructions
        then  = []
        then += self.dispatch(n.then, target)
        then += [Jump86(EndIfLStr)]
        # Else Instructions
        else_ = []
        else_ += [Label86(ElseLStr)]
        else_ += self.dispatch(n.else_, target)
        else_ += [Label86(EndIfLStr)]
        return (test + [If86(then, else_)])

    def visitCallFunc(self, n, target):
        instrs = []
        cntargs = 0
        n.args.reverse()
        for arg in n.args:
            cntargs += 1
            instrs += [Push86(arg_select(arg))]
        instrs += [Call86(n.node.name)]
        instrs += [Move86(EAX, target)]
        if(cntargs > 0):
            instrs += [Add86(Const86(WORDLEN * cntargs), ESP)]
        return instrs

    def visitflat_InstrSeq(self, n, target):
        instrs = []
        for node in n.nodes:
            instrs += self.dispatch(node)
        instrs += [Move86(Var86(n.expr.name), target)]
        return instrs
