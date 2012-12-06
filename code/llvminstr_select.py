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
import platform

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
ICMPTEMP     = "icmptemp"

(bits, linkage) = platform.architecture()
if(bits == '32bit'):
    DEFAULTTYPE = I32
elif(bits == '64bit'):
    DEFAULTTYPE = I64
else:
    raise Exception("Unknown bits type")

DEFAULTZERO  = ConstLLVM(0, DEFAULTTYPE)
DEFAULTONE   = ConstLLVM(1, DEFAULTTYPE)
DEFAULTFALSE = DEFAULTZERO
DEFAULTTRUE  = DEFAULTONE

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
        instrs = []
        blocks = []
        thisL = LabelArgLLVM(LocalLLVM(generate_label("block")))
        nextL = LabelArgLLVM(LocalLLVM(generate_label("block")))
        length = len(n.nodes)
        if(length > 0):
            # None-Empty List
            for node in n.nodes:
                ret = self.dispatch(node, func)
                if(isinstance(ret[0], BlockLLVMInst)):
                    # If list of blocks returned
                    # Add jump to start of first returned block
                    instrs += [switchLLVM(DEFAULTZERO, ret[0].label, [])]
                    # Add new block
                    blocks += [blockLLVM(thisL, instrs)]
                    # Patch in proper destination in last block
                    ret[-1].instrs[-1].defaultDest = nextL
                    # Add returned blocks
                    blocks += ret
                    # Reset instructiosn and update labels
                    instrs = []
                    thisL = nextL
                    nextL = LabelArgLLVM(LocalLLVM(generate_label("block")))
                elif(isinstance(ret[0], LLVMInst)):
                    # If list of instructions returned
                    instrs += ret
                    if((node is n.nodes[-1]) and not(isinstance(instrs[-1], TermLLVMInst))):
                        # If this is the last node and no terminal instruction has been reached
                        instrs += [switchLLVM(DEFAULTZERO, DUMMYL, [])]
                        
                    if(isinstance(instrs[-1], TermLLVMInst)):
                        # If last instruction returned is terminal, end block
                        blocks += [blockLLVM(thisL, instrs)]
                        instrs = []
                        thisL = nextL
                        nextL = LabelArgLLVM(LocalLLVM(generate_label("block")))
                else:
                    raise Exception("Unhandled return type")
        else:
            # Empty List
            # Add Dummy Block (will be patched into soemthing usefull later)
            blocks += [blockLLVM(DUMMYL, [switchLLVM(DEFAULTZERO, DUMMYL, [])])]
        return blocks

    def visitVarAssign(self, n, func):
        target = VarLLVM(LocalLLVM(n.target), DEFAULTTYPE)
        return (self.dispatch(n.value, target))

    def visitDiscard(self, n, func):
        target = VarLLVM(LocalLLVM(generate_name(DISCARDTEMP)), DEFAULTTYPE)
        return (self.dispatch(n.expr, target))

    def visitReturn(self, n, func):
        (name, _type) = func
        val = self.dispatch(n.value)
        if(_type != getType(val)):
            raise Exception("Return type must match function type")
        return ([retLLVM(val)])

    def visitWhileFlatPhi(self, n, func):
        # Setup Values
        testVal =  self.dispatch(n.test)
        # Setup Labels
        entryL = LabelArgLLVM(LocalLLVM(generate_label("wentry")))
        testprepL = LabelArgLLVM(LocalLLVM(generate_label("wtestprep")))
        testL = LabelArgLLVM(LocalLLVM(generate_label("wtest")))
        loopL = LabelArgLLVM(LocalLLVM(generate_label("wloop")))
        elseL = LabelArgLLVM(LocalLLVM(generate_label("welse")))
        endL  = LabelArgLLVM(LocalLLVM(generate_label("wend")))
        # Loop Block
        loopB   = self.dispatch(n.body, None)
        # Patch in proper label for first block
        loopB[0].label = loopL
        # Patch in proper destination in last block
        loopB[-1].instrs[-1].defaultDest = testprepL
        # Entry Block
        entryI    = []
        entryI   += [switchLLVM(DEFAULTZERO, testprepL, [])]
        entryB    = [blockLLVM(entryL, entryI)]
        # TestPrep Block
        phis = []
        for key in n.phi:
            values = n.phi[key]
            prePhi = PhiPairLLVM(self.dispatch(Name(values[0])), 
                                 entryL)
            postPhi = PhiPairLLVM(self.dispatch(Name(values[1])),
                                  loopB[-1].label)
            target = VarLLVM(LocalLLVM(key), DEFAULTTYPE)
            phis += [phiLLVM(target, [prePhi, postPhi])]
        testprepB = self.dispatch(n.testss, None)
        testprepB[0].instrs = phis + testprepB[0].instrs
        testprepB[0].label = testprepL
        testprepB[-1].instrs[-1].defaultDest = testL

        # Test Block
        loopS = SwitchPairLLVM(DEFAULTTRUE, loopL)
        testI   = []
        testI  += [switchLLVM(testVal, elseL, [loopS])]
        testB   = [blockLLVM(testL, testI)]
        # Else Block
        if n.else_:
            elseB   = self.dispatch(n.else_, None)
            # Patch in proper label for first block
            elseB[0].label = elseL
            # Patch in proper destination in last block
            elseB[-1].instrs[-1].defaultDest = endL
        else:
            elseI    = []
            elseI   += [switchLLVM(DEFAULTZERO, endL, [])]
            elseB    = [blockLLVM(elseL, elseI)]
        # Test Block
        endI    = []
        endI   += [switchLLVM(DEFAULTZERO, DUMMYL, [])]
        endB    = [blockLLVM(endL, endI)]
        return entryB + testprepB + testB + loopB + elseB + endB

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
        tmp = VarLLVM(LocalLLVM(generate_name(ICMPTEMP)), LLVMBOOLTYPE)
        instrs = []
        instrs += [icmpLLVM(tmp, ICMP_EQ, left, right)]
        instrs += [zextLLVM(target, tmp, DEFAULTTYPE)]
        return instrs

    def visitIntNotEqual(self, n, target):
        left  = self.dispatch(n.left)
        right = self.dispatch(n.right)
        tmp = VarLLVM(LocalLLVM(generate_name(ICMPTEMP)), LLVMBOOLTYPE)
        instrs = []
        instrs += [icmpLLVM(tmp, ICMP_NE, left, right)]
        instrs += [zextLLVM(target, tmp, DEFAULTTYPE)]
        return instrs

    def visitIntUnarySub(self, n, target):
        left = DEFAULTZERO
        right = self.dispatch(n.expr)
        return [subLLVM(target, left, right)]

    def visitIfExpFlat(self, n, target):
        # Setup Values
        testVal =  self.dispatch(n.test)
        thenVal =  self.dispatch(n.then.expr)
        elseVal =  self.dispatch(n.else_.expr)
        # Setup Labels
        testL = LabelArgLLVM(LocalLLVM(generate_label("test")))
        thenL = LabelArgLLVM(LocalLLVM(generate_label("then")))
        elseL = LabelArgLLVM(LocalLLVM(generate_label("else")))
        endL  = LabelArgLLVM(LocalLLVM(generate_label("end")))
        # Test Block
        thenS = SwitchPairLLVM(DEFAULTTRUE, thenL)
        testI   = []
        testI  += [switchLLVM(testVal, elseL, [thenS])]
        testB   = [blockLLVM(testL, testI)]
        # Then Block
        thenB   = self.dispatch(n.then.node, None)
        # Patch in proper label for first block
        thenB[0].label = thenL
        # Patch in proper destination in last block
        thenB[-1].instrs[-1].defaultDest = endL
        # Else Block
        #elseI   = []
        elseB   = self.dispatch(n.else_.node, None)
        # Patch in proper label for first block
        elseB[0].label = elseL
        # Patch in proper destination in last block
        elseB[-1].instrs[-1].defaultDest = endL
        # End Block
        thenP = PhiPairLLVM(thenVal, thenB[-1].label)
        elseP = PhiPairLLVM(elseVal, elseB[-1].label)
        endI    = []
        endI   += [phiLLVM(target, [thenP, elseP])]
        endI   += [switchLLVM(DEFAULTZERO, DUMMYL, [])]
        endB    = [blockLLVM(endL, endI)]
        return testB + thenB + elseB + endB

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
