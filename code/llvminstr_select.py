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
from utilities import generate_label
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
DUMMYL = LabelArgLLVM(LocalLLVM("DUMMY_L"))

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
        blocks = self.dispatch(n.code, (name, _type))
        return defineLLVM(_type, GlobalLLVM(name), args, blocks)
        
    # Statements    

    def visitStmtList(self, n, func):
        blocks = []
        instrs = []
        thisL = LabelArgLLVM(LocalLLVM(generate_label("block")))
        nextL = LabelArgLLVM(LocalLLVM(generate_label("block")))
        for node in n.nodes:
            (ret, blocked) = self.dispatch(node, func)
            if(blocked):
                # If list of blocks returned
                # Add jump to start of first returned block
                instrs += [switchLLVM(LLVMZERO, ret[0].label, [])]
                # Add new block
                blocks += [blockLLVM(thisL, instrs)]
                # Patch in proper label for jump in last block
                ret[-1].instrs[-1].defaultDest = nextL
                # Add returned blocks
                blocks += ret
                # Reset instructiosn and update labels
                instrs = []
                thisL = nextL
                nextL = LabelArgLLVM(LocalLLVM(generate_label("block")))
            else:
                # If list of instructions returned
                instrs += ret
                # If last instruction returned is terminal, end block
                if(isinstance(instrs[-1], TermLLVMInst)):
                    blocks += [blockLLVM(thisL, instrs)]
                    instrs = []
                    thisL = nextL
                    nextL = LabelArgLLVM(LocalLLVM(generate_label("block")))
        return blocks

    def visitVarAssign(self, n, func):
        target = VarLLVM(LocalLLVM(n.target), DEFAULTTYPE)
        if(isinstance(n.value, IfExpFlat)):
            return (self.dispatch(n.value, target), True)
        else:
            return (self.dispatch(n.value, target), False)

    def visitDiscard(self, n, func):
        target = VarLLVM(LocalLLVM(generate_name(DISCARDTEMP)), DEFAULTTYPE)
        if(isinstance(n.expr, IfExpFlat)):
            return (self.dispatch(n.expr, target), True)
        else:
            return (self.dispatch(n.expr, target), False)

    def visitReturn(self, n, func):
        (name, _type) = func
        val = self.dispatch(n.value)
        if(_type != getType(val)):
            raise Exception("Return type must match function type")
        return ([retLLVM(val)], False)

    def visitWhileFlatPhi(self, n, func):
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

    def visitIfPhi(self, n, func_name):
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
    
    # Terminal Expressions

    def visitConst(self, n):
        return ConstLLVM(n.value, DEFAULTTYPE)

    def visitName(self, n):
        return VarLLVM(LocalLLVM(n.name), DEFAULTTYPE)

    # Non-Terminal Expressions

    def visitIntAdd(self, n, target):
        left  = self.dispatch(n.left)
        right = self.dispatch(n.right)
        return [addLLVM(target, left, right)]
        
    def visitIntEqual(self, n, target):
        left  = self.dispatch(n.left)
        right = self.dispatch(n.right)
        return [icmpLLVM(target, ICMP_EQ, left, right)]

    def visitIntNotEqual(self, n, target):
        left  = self.dispatch(n.left)
        right = self.dispatch(n.right)
        return [icmpLLVM(target, ICMP_NE, left, right)]

    def visitIntUnarySub(self, n, target):
        left = LLVMZERO
        right = self.dispatch(n.expr)
        return [subLLVM(target, left, right)]

    def visitIfExpFlat(self, n, target):
        raise Exception("IfExpFlat Not Yet Working")
        # Setup Values
        testVal =  self.dispatch(n.test)
        thenVal =  self.dispatch(n.then.expr)
        elseVal =  self.dispatch(n.else_.expr)
        # Setup Labels
        testL = LabelArgLLVM(LocalLLVM(generate_label("test")))
        thenL = LabelArgLLVM(LocalLLVM(generate_label("then")))
        thenP = PhiPairLLVM(thenVal, thenL)
        thenS = SwitchPairLLVM(LLVMTRUE, thenL)
        elseL = LabelArgLLVM(LocalLLVM(generate_label("else")))
        elseP = PhiPairLLVM(elseVal, elseL)
        endL  = LabelArgLLVM(LocalLLVM(generate_label("end")))
        # Test Block
        testI   = []
        testI  += [switchLLVM(testVal, elseL, [thenS])]
        testB   = blockLLVM(testL, testI)
        # Then Block
        thenI   = []
        for node in n.then.node.nodes:
            thenI += self.dispatch(node, None)
        thenI  += [switchLLVM(LLVMZERO, endL, [])]
        thenB   = blockLLVM(thenL, thenI)
        # Else Block
        elseI   = []
        for node in n.else_.node.nodes:
            elseI += self.dispatch(node, None)
        elseI  += [switchLLVM(LLVMZERO, endL, [])]
        elseB   = blockLLVM(elseL, elseI)
        # End Block
        endI    = []
        endI   += [phiLLVM(target, [thenP, elseP])]
        endI   += [switchLLVM(LLVMZERO, DUMMYL, [])]
        endB    = blockLLVM(endL, endI)
        return [testB, thenB, elseB, endB]

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
