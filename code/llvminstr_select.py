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
        self.stringsInstr = []

    def preorder(self, tree, *args):
        ret = self.stringsInstr + super(LLVMInstrSelectVisitor, self).preorder(tree)
        print ret
        return ret
        
    # Modules

    def visitProgram(self, n):
        slambdas = []
        for node in n.nodes:
            slambdas += [self.dispatch(node)]
        return slambdas

    def visitSLambda(self, n):
        _type = DEFAULTTYPE
        name  = n.label
        args = []
        for param in n.params:
            args  += [VarLLVM(LocalLLVM(param), DEFAULTTYPE)]
        blocks = self.dispatch(n.code, (name, _type))
        # Fix up functions with no return
        if(isinstance(blocks[-1].instrs[-1], TermLLVMInst)):
            if(not isinstance(blocks[-1].instrs[-1], retLLVM)):
                blocks[-1].instrs[-1] = retLLVM(DEFAULTZERO)
        else:
            raise Exception("Each block must end with a termianl instruction")
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
        blocks = []
        phis = {}
        # Setup Labels
        nextL = LabelArgLLVM(LocalLLVM(generate_label("if")))    
        endL  = LabelArgLLVM(LocalLLVM(generate_label("end")))
        # Tests
        for test in n.tests:
            (test, tbody, phiD) = test
            testV   =  self.dispatch(test)
            testB   =  self.dispatch(tbody, func_name)
            testL   =  nextL
            nextL   =  LabelArgLLVM(LocalLLVM(generate_label("if")))
            testS   =  SwitchPairLLVM(DEFAULTTRUE, testB[0].label)
            testI   =  [switchLLVM(testV, nextL, [testS])]
            for key in phiD.keys():
                phiV = VarLLVM(LocalLLVM(phiD[key]), DEFAULTTYPE)
                phiP = [PhiPairLLVM(phiV, testB[-1].label)]
                if key in phis:
                    phis[key] += phiP
                else:
                    phis[key] =  phiP
            testB[-1].instrs[-1].defaultDest = endL
            blocks  += [blockLLVM(testL, testI)] + testB
        # Else
        (ebody, phiD) = n.else_
        elseB   =  self.dispatch(ebody, func_name)
        elseL   = nextL
        nextL   =  LabelArgLLVM(LocalLLVM(generate_label("if")))
        elseI   =  [switchLLVM(DEFAULTZERO, elseB[0].label, [])]
        for key in phiD.keys():
            phiV = VarLLVM(LocalLLVM(phiD[key]), DEFAULTTYPE)
            phiP = [PhiPairLLVM(phiV, elseB[-1].label)]
            if key in phis:
                phis[key] += phiP
            else:
                phis[key] =  phiP
        elseB[-1].instrs[-1].defaultDest = endL
        blocks  += [blockLLVM(elseL, elseI)] + elseB
        # End
        endI    =  []
        for key in phis.keys():
            phiT =  VarLLVM(LocalLLVM(key), DEFAULTTYPE)
            endI += [phiLLVM(phiT, phis[key])]
        endI    += [switchLLVM(DEFAULTZERO, DUMMYL, [])]
        blocks  +=  [blockLLVM(endL, endI)]
        return blocks
    
    # Terminal Expressions

    def visitConst(self, n):
        return ConstLLVM(n.value, DEFAULTTYPE)

    def visitName(self, n):
        return VarLLVM(LocalLLVM(n.name), DEFAULTTYPE)

    def visitString(self, n):
        raise Exception("You should not have come here, Frodo")
        # stringArray = LLVMArray(len(n.string), I8)
        # print stringArray
        # actualString = LLVMString(stringArray, n.string)
        # print actualString
        # tmp = VarLLVM(GlobalLLVM(generate_name("stringName")), stringArray)
        # print tmp
        # stringDeclare = declareLLVMString(tmp, actualString)
        # print stringDeclare
        # self.stringsInstr += [stringDeclare]

        # cast = getelementptrLLVM(VarLLVM(LocalLLVM(generate_name("cast")), PI8), tmp, [DEFAULTZERO, DEFAULTZERO])
        # print cast

        # return cast

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
        instrList = []
        args = []
        # print "target " + str(target)
        for arg in n.args:
            if isinstance(arg, SLambdaLabel):
                name = generate_name("instrsel_SLamdaLabel")
                numargs = 0
                temp = VarLLVM(LocalLLVM(name), DEFAULTTYPE)
                # print "temp  " + str(temp)
                # print "SLambdaLabel: "+ str(arg) + "args "+ str(arg.numargs)
                arg_types = LLVMFuncPtrType(DEFAULTTYPE, DEFAULTTYPE, arg.numargs)
                print arg_types
                value = VarLLVM(GlobalLLVM(arg.name),arg_types)
                instrList += [ptrtointLLVM(temp, value, DEFAULTTYPE)]
                args += [temp]
            #%fptr1  = ptrtoint i64 (i64)* @ftest to i64
            elif isinstance(arg, String):
                stringArray = LLVMArray(len(arg.string), I8)
                # print stringArray
                actualString = LLVMString(stringArray, arg.string)
                # print actualString
                tmp = VarLLVM(GlobalLLVM(generate_name("stringName")), stringArray)
                # print "tm" + str(tmp)
                stringDeclare = declareLLVMString(tmp, actualString)
                # print stringDeclare
                self.stringsInstr += [stringDeclare]
                placeholder = VarLLVM(LocalLLVM(generate_name("cast")), PI8)
                # print "placeholder" + str(placeholder)
                cast = getelementptrLLVM(placeholder, tmp, [DEFAULTZERO, DEFAULTZERO])
                # print cast
                instrList += [cast]
                args += [placeholder]
            else:
                # print "here"
                args += [self.dispatch(arg)]
        # print "args" + str(args)
        instrList += [callLLVM(DEFAULTTYPE, GlobalLLVM(n.node.name), args, target)]
        # print instrList
        return instrList
        
    def visitIndirectCallFunc(self, n, target):
        #%fptr3  = inttoptr i64 %fptr2 to i64 (i64)*
        #%res0   = call i64 %fptr3(i64 5)
        args = []
        instrList = []
        for arg in n.args:
            args += [self.dispatch(arg)]
        arg_types = LLVMFuncPtrType(DEFAULTTYPE, DEFAULTTYPE, len(n.args))
        tmp = VarLLVM(LocalLLVM(generate_name("inttoptrConversion")), DEFAULTTYPE)
        instrList += [inttoptrLLVM(tmp, VarLLVM(LocalLLVM(n.node.name), DEFAULTTYPE), arg_types)]
        instrList += [callLLVM(DEFAULTTYPE, getArg(tmp), args, target)]
        return instrList
