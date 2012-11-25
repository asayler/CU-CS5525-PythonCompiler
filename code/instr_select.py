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
from pyast import *
from x86ast import *
from stringfind import *

# Helper Tools
from vis import Visitor

from utilities import generate_name
from utilities import generate_return_label

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

IfThenLabelCnt = 1
WhileLabelCnt = 1
ELSELABEL  = "l_else"
ENDIFLABEL = "l_endelse"
CASELABEL = 'l_case'
WHILESTARTLABEL = "l_whilestart"
WHILEENDLABEL   = "l_whileend"

class InstrSelectVisitor(Visitor):
    # ToDo: Make inherit from CopyVisitor?

    def __init__(self):
        super(InstrSelectVisitor,self).__init__()
        #del CopyVisitor.visitWhile
    # Modules

    def preorder(self, tree, *args):
        strings = StringFindVisitor().preorder(tree)
        return (strings, super(InstrSelectVisitor, self).preorder(tree))

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
        ret.params = n.params
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
        global WhileLabelCnt
        WhileStartLStr  = WHILESTARTLABEL + str(WhileLabelCnt)
        WhileEndLStr    = WHILEENDLABEL   + str(WhileLabelCnt)
        WhileLabelCnt += 1
        # Test Instructions
        testtmp = Var86(generate_name(WHILETESTTMP))
        test  = []
        test += [Label86(WhileStartLStr)]
        test += self.dispatch(n.testss, funcName)
        test += self.dispatch(n.test, testtmp)
        test += [Comp86(x86FALSE, testtmp)]
        test += [JumpEqual86(WhileEndLStr)]
        # Body Instructions
        body  = []
        body += self.dispatch(n.body, funcName)
        body += [Jump86(WhileStartLStr)]
        body += [Label86(WhileEndLStr)]
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

    def visitIf(self, n, func_name):
        #Setup Label
        global IfThenLabelCnt
        caselabels = [('%s%d_%d' % (ELSELABEL, i, IfThenLabelCnt)) for i in xrange(0, len(n.tests))]
        EndIfLStr = ENDIFLABEL + str(IfThenLabelCnt)
        IfThenLabelCnt += 1
        def make_branches(testlist, caselabels, else_):
            if testlist:
                test, body = testlist[0]
                tmp = Var86(generate_name(IFTEMP))
                tinstrs = self.dispatch(test, tmp)
                tinstrs += [Comp86(x86FALSE, tmp)]
                tinstrs += [JumpEqual86(caselabels[0])]
                
                ninstrs = self.dispatch(body, func_name)
                ninstrs += [Jump86(EndIfLStr)]
                
                einstrs = [Label86(caselabels[0])] + make_branches(testlist[1:], caselabels[1:], else_)
                return tinstrs + [If86(ninstrs, einstrs)]
            else:
                instrs = self.dispatch(else_, func_name)
                instrs += [Label86(EndIfLStr)]
                return instrs
        return make_branches(n.tests, caselabels, n.else_)

    def visitIfExpFlat(self, n, target):
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
