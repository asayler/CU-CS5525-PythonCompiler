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

# Data Types
from pyast import *
from llvmast import *

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

DEFAULTTYPE = I64

class LLVMInstrSelectVisitor(Visitor):

    def __init__(self):
        super(LLVMInstrSelectVisitor, self).__init__()

    # Modules

    # All of these still need updateed, currently just x86 copies

    def visitProgram(self, n):
        slambdas = []
        for node in n.nodes:
            slambdas += [self.dispatch(node)]
        return slambdas

    def visitSLambda(self, n):
        _type = DEFAULTTYPE
        name  = n.label
        args  = n.params
        instrs = []#self.dispatch(n.code, n.label)
        return DefineLLVM(_type, name, args, instrs)
        
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
