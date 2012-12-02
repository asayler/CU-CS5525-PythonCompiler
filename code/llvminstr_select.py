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

    def visitProgram(self, n):
        slambdas = []
        for node in n.nodes:
            slambdas += [self.dispatch(node)]
        return slambdas

    def visitSLambda(self, n):
        _type = DEFAULTTYPE
        name  = n.label
        args  = n.params
        instrs = self.dispatch(n.code, (name, _type))
        return DefineLLVM(_type, GlobalLLVM(name), args, instrs)
        
    # Statements    

    def visitStmtList(self, n, func):
        instrs = []
        for node in n.nodes:
            instrs += self.dispatch(node, func)
        return instrs

    def visitVarAssign(self, n, func):
        return self.dispatch(n.value, VarLLVM(LocalLLVM(n.target), DEFAULTTYPE))

    def visitDiscard(self, n, func):
        tmp = VarLLVM(LocalLLVM(generate_name(DISCARDTEMP)), DEFAULTTYPE)
        return self.dispatch(n.expr, tmp)

    def visitReturn(self, n, func):
        (name, _type) = func
        val = self.dispatch(n.value)
        if(_type != val.type):
            raise Exception("Return type must match function type")
        return [retLLVM(val)]

    def visitWhileFlat(self, n, func):
        raise Exception("Not Yet Implemented")
        #Setup Label
        whileStartL, whileEndL = generate_while_labels()
        # Test Instructions
        testtmp = Var86(generate_name(WHILETESTTMP))
        test  = []
        test += [Label86(whileStartL)]
        test += self.dispatch(n.testss, func)
        test += self.dispatch(n.test, testtmp)
        test += [Comp86(x86FALSE, testtmp)]
        test += [JumpEqual86(whileEndL)]
        # Body Instructions
        body  = []
        body += self.dispatch(n.body, func)
        body += [Jump86(whileStartL)]
        body += [Label86(whileEndL)]
        return [Loop86(test, body)]
    
    # Terminal Expressions

    def visitConst(self, n):
        return ConstLLVM(n.value, DEFAULTTYPE)
        #return [Move86(Const86(n.value), target)]

    def visitName(self, n):
        return VarLLVM(LocalLLVM(n.name), DEFAULTTYPE)
        #return [Move86(Var86(n.name), target)]

    # Non-Terminal Expressions

    def visitIntAdd(self, n, target):
        raise Exception("Not Yet Implemented")
        instrs = []
        instrs += [Move86(arg_select(n.left), target)]
        instrs += [Add86(arg_select(n.right), target)]
        return instrs

    def visitIntEqual(self, n, target):
        raise Exception("Not Yet Implemented")
        instrs = []
        instrs += [Move86(arg_select(n.left), target)]
        instrs += [Comp86(arg_select(n.right), target)]
        # prezero register (avoids call to movebzl)
        instrs += [Move86(x86ZERO, target)]
        instrs += [SetEq86(target)]
        return instrs

    def visitIntNotEqual(self, n, target):
        raise Exception("Not Yet Implemented")
        instrs = []
        instrs += [Move86(arg_select(n.left), target)]
        instrs += [Comp86(arg_select(n.right), target)]
        # prezero register (avoids call to movebzl)
        instrs += [Move86(x86ZERO, target)]
        instrs += [SetNEq86(target)]
        return instrs

    def visitIntUnarySub(self, n, target):
        raise Exception("Not Yet Implemented")
        instrs = []
        instrs += [Move86(arg_select(n.expr), target)]
        instrs += [Neg86(target)]
        return instrs

    def visitIf(self, n, func_name):
        raise Exception("Not Yet Implemented")
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
        raise Exception("Not Yet Implemented")
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
        args = []
        for arg in n.args:
            args += [self.dispatch(arg)]
        return [callLLVM(DEFAULTTYPE, GlobalLLVM(n.node.name), args, target)]
        
    def visitIndirectCallFunc(self, n, target):
        raise Exception("Not Yet Implemented")
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
        raise Exception("Not Yet Implemented")
        instrs = self.dispatch(n.node, None)
        instrs += [Move86(Var86(n.expr.name), target)]
        return instrs
