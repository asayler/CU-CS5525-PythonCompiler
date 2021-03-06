# CU CS5525
# Fall 2012
# GSV Python Compiler
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

# Data Types
from pyast import *
from x86ast import *

# Parents
from vis import Visitor

# Helper Tools
from stringfind import StringFindVisitor

from utilities import generate_name
from utilities import generate_return_label
from utilities import generate_while_labels
from utilities import generate_if_labels

def arg_select(ast):
    if isinstance(ast, Name):
        return Var86(ast.name)
    elif isinstance(ast, Const):
        return Const86(ast.value)
    elif isinstance(ast, SLambdaLabel):
        return IndirectJumpLabel86(ast.name)
    elif isinstance(ast, String):
        return Const86(ast.location)
    else:
        raise Exception("InstrSelect: Invalid argument - " + str(ast))

DISCARDTEMP = "discardtemp"
NULLTEMP = "nulltemp"
IFTEMP = "iftemp"
WHILETESTTMP = "whiletesttmp"

class x86InstrSelectVisitor(Visitor):

    def __init__(self):
        super(x86InstrSelectVisitor, self).__init__()

    def preorder(self, tree, *args):
        strings = StringFindVisitor().preorder(tree)
        return (strings, super(x86InstrSelectVisitor, self).preorder(tree))

    # Modules

    def visitProgram(self, n):
        slambdas = []
        for node in n.nodes:
            slambdas += [self.dispatch(node)]
        return slambdas

    def visitSLambda(self, n):
        instrs = []
        # Handle Arguments
        offset = 8
        for param in n.params:
            instrs += [Move86(Mem86(offset, EBP), Var86(param))]
            offset += 4
        instrs += self.dispatch(n.code, n.label)
        ret = Func86(n.label, instrs)
        return ret

    # Statements    

    def visitStmtList(self, n, funcName):
        instrs = []
        for s in n.nodes:
            instrs += self.dispatch(s, funcName)
        return instrs

    def visitVarAssign(self, n, funcName):
        return self.dispatch(n.value, Var86(n.target))

    def visitDiscard(self, n, funcName):
        tmp = Var86(generate_name(DISCARDTEMP))
        return self.dispatch(n.expr, tmp)

    def visitReturn(self, n, funcName):
        if(funcName == None):
            raise Exception("Return must have a valid function name")
        instrs = []
        instrs += [Move86(arg_select(n.value), EAX)]
        instrs += [Jump86(generate_return_label(funcName))]
        return instrs

    def visitWhileFlat(self, n, funcName):
        #Setup Label
        whileStartL, whileEndL = generate_while_labels()
        # Test Instructions
        testtmp = Var86(generate_name(WHILETESTTMP))
        test  = []
        test += [Label86(whileStartL)]
        test += self.dispatch(n.testss, funcName)
        test += self.dispatch(n.test, testtmp)
        test += [Comp86(x86FALSE, testtmp)]
        test += [JumpEqual86(whileEndL)]
        # Body Instructions
        body  = []
        body += self.dispatch(n.body, funcName)
        body += [Jump86(whileStartL)]
        body += [Label86(whileEndL)]
        return [Loop86(test, body)]
    
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

    def visitIntCmp(self, n, target):
        if(n.op == PY_EQ):
            op = X86_EQ
        elif(n.op == PY_NE):
            op = X86_NE
        elif(n.op == PY_GT):
            op = X86_GT
        elif(n.op == PY_GE):
            op = X86_GE
        elif(n.op == PY_LT):
            op = X86_LT
        elif(n.op == PY_LE):
            op = X86_LE
        else:
            raise Exception("Unknown op in IntCmp")
        instrs = []
        instrs += [Move86(arg_select(n.left), target)]
        instrs += [Comp86(arg_select(n.right), target)]
        # prezero register (avoids call to movebzl)
        instrs += [Move86(x86ZERO, target)]
        instrs += [SetCmp86(op, target)]
        return instrs

    def visitIntUnarySub(self, n, target):
        instrs = []
        instrs += [Move86(arg_select(n.expr), target)]
        instrs += [Neg86(target)]
        return instrs

    def visitIf(self, n, func_name):
        #Setup Label
        caseLs, endIfL = generate_if_labels(len(n.tests))
        def make_branches(testlist, caseLs, else_):
            if testlist:
                test, body = testlist[0]
                tmp = Var86(generate_name(IFTEMP))
                tinstrs = self.dispatch(test, tmp)
                tinstrs += [Comp86(x86FALSE, tmp)]
                tinstrs += [JumpEqual86(caseLs[0])]
                
                ninstrs = self.dispatch(body, func_name)
                ninstrs += [Jump86(endIfL)]
                
                einstrs = [Label86(caseLs[0])] + make_branches(testlist[1:], caseLs[1:], else_)
                return tinstrs + [If86(ninstrs, einstrs)]
            else:
                instrs = self.dispatch(else_, func_name)
                instrs += [Label86(endIfL)]
                return instrs
        return make_branches(n.tests, caseLs, n.else_)

    def visitIfExpFlat(self, n, target):
        #Setup Label
        caseLs, endIfL = generate_if_labels(1)
        elseL = caseLs[0]
        # Test Instructions
        test  = []
        test += self.dispatch(n.test, target)
        test += [Comp86(x86FALSE, target)]
        test += [JumpEqual86(elseL)]
        # Then Instructions
        then  = []
        then += self.dispatch(n.then, target)
        then += [Jump86(endIfL)]
        # Else Instructions
        else_ = []
        else_ += [Label86(elseL)]
        else_ += self.dispatch(n.else_, target)
        else_ += [Label86(endIfL)]
        return (test + [If86(then, else_)])

    def visitCallFunc(self, n, target):
        instrs = []
        cntargs = 0
        align = (STACKALIGN - (len(n.args) % STACKALIGN))
        align %= STACKALIGN
        offset = 0
        if align != 0:
            offset += WORDLEN * align
            instrs += [Sub86(Const86(offset), ESP)]
        n.args.reverse()
        for arg in n.args:
            cntargs += 1
            instrs += [Push86(arg_select(arg))]
            offset += WORDLEN
        instrs += [Call86(n.node.name)]
        instrs += [Move86(EAX, target)]
        if(offset > 0):
            instrs += [Add86(Const86(offset), ESP)]
        return instrs

    def visitIndirectCallFunc(self, n, target):
        instrs = []
        instrs += self.dispatch(n.node, target)
        cntargs = 0
        align = (STACKALIGN - (len(n.args) % STACKALIGN))
        offset = 0
        if align != 0:
            offset += WORDLEN * align
            instrs += [Sub86(Const86(offset), ESP)]
        n.args.reverse()
        for arg in n.args:
            cntargs += 1
            instrs += [Push86(arg_select(arg))]
            offset += WORDLEN
        instrs += [IndirectCall86(target)]
        instrs += [Move86(EAX, target)]
        if(cntargs > 0):
            instrs += [Add86(Const86(offset), ESP)]
        return instrs

    def visitInstrSeq(self, n, target):
        instrs = self.dispatch(n.node, None)
        instrs += [Move86(Var86(n.expr.name), target)]
        return instrs
