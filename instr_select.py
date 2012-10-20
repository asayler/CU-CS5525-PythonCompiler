# CU CS5525
# Fall 2012
# Python Compiler
#
# instr_select.py
# Visitor Funcations for x86 Instruction Selection
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

    def visitIntAdd(self, n, target):
        instrs = []
        instrs += [Move86(arg_select(n.left), target)]
        instrs += [Add86(arg_select(n.right), target)]
        return instrs

    def visitIntEqual(self, n, target):
        instrs = []
        instrs += [Move86(arg_select(n.left), target)]
        instrs += [Comp86(arg_select(n.right), target)]
        # prezero register (avoids call to movebzl)
        instrs += [Move86(x86ZERO, target)]
        instrs += [SetEq86(target)]
        return instrs

    def visitIntNotEqual(self, n, target):
        instrs = []
        instrs += [Move86(arg_select(n.left), target)]
        instrs += [Comp86(arg_select(n.right), target)]
        # prezero register (avoids call to movebzl)
        instrs += [Move86(x86ZERO, target)]
        instrs += [SetNEq86(target)]
        return instrs

    def visitIntUnarySub(self, n, target):
        instrs = []
        instrs += [Move86(arg_select(n.expr), target)]
        instrs += [Neg86(target)]
        return instrs

    def visitIfExp(self, n, target):
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

    def visitInstrSeq(self, n, target):
        instrs = []
        for node in n.nodes:
            instrs += self.dispatch(node)
        instrs += [Move86(Var86(n.expr.name), target)]
        return instrs
