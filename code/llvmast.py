# CU CS5525
# Fall 2012
# GSV Python Compiler
#
# llvmast.py
# LLVM Instruction AST Nodes
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

"""LLVM AST tree nodes"""

# LLVM Constants and Aliases
ICMP_EQ  = "eq"
ICMP_NE  = "ne"
ICMP_UGT = "ugt"
ICMP_UGE = "uge"
ICMP_ULT = "ult"
ICMP_ULE = "ule"
ICMP_SGT = "sgt"
ICMP_SGE = "sge"
ICMP_SLT = "slt"
ICMP_SLE = "sle"

# LLVM Types

class LLVMType(object):
    def __hash__(self):
        return hash(self.__repr__())
    def __eq__(self, that):
        return self.__repr__() == that.__repr__()

class LLVMVoid(LLVMType):
    def __init__(self):
        pass
    def __repr__(self):
        return ('void')
    
class LLVMInt(LLVMType):
    def __init__(self, length):
        self.length = length
    def __repr__(self):
        return ('i%d' % (self.length))    

class LLVMPointer(LLVMType):
    def __init__(self, _type):
        self.type = _type
    def __repr__(self):
        return ('%s*' % (str(self.type)))

class LLVMLabel(LLVMType):
    def __init__(self):
        pass
    def __repr__(self):
        return ('label')

class LLVMArray(LLVMType):
    def __init__(self, numelem, _type):
        self.numelem = numelem
        self.type = _type
    def __repr__(self):
        return ('[%d x %s]' % (self.numelem, str(self.type)))


I1   = LLVMInt(1)
I8   = LLVMInt(8)
I32  = LLVMInt(32)
I64  = LLVMInt(64)
PI8  = LLVMPointer(I8)
PI32 = LLVMPointer(I32)
PI64 = LLVMPointer(I64)

LLVMBOOLTYPE = I1

class LLVMFuncPtrType(LLVMType):
    def __init__(self, ret, typeargs, numargs):
        self.ret = ret
        self.args = []
        n = numargs
        while(n>0):
            self.args += [typeargs]
            n -= 1

    def __repr__(self):
        return ("%s (%s)*" % (str(self.ret),
                              ", ".join(map(lambda x: str(x), self.args))))

class LLVMString(LLVMType):
    def __init__(self, _type, _str):
        self.type = _type
        self.str = _str
    def __repr__(self):
        return ("%s c\"%s\00\"") % (self.type, self.str)

# LLVM Names

class LLVMName(object):
    def __hash__(self):
        return hash(self.__repr__())
    def __eq__(self, that):
        return self.__repr__() == that.__repr__()

class GlobalLLVM(LLVMName):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "@%s" % (str(self.name))

class LocalLLVM(LLVMName):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "%%%s" % (str(self.name))

# LLVM Primitive Args

class LLVMArg(object):
    def __hash__(self):
        return hash(self.__repr__())
    def __eq__(self, that):
        return self.__repr__() == that.__repr__()
    
class ConstLLVM(LLVMArg):
    def __init__(self, value, _type):
        self.value = value
        self.type = _type
    def __repr__(self):
        return "%s %d" % (str(self.type), self.value)

class VarLLVM(LLVMArg):
    def __init__(self, name, _type):
        self.name = name
        self.type = _type
    def __repr__(self):
        return "%s %s" % (str(self.type), str(self.name))

class LabelArgLLVM(LLVMArg):
    def __init__(self, name):
        self.name = name
        self.type = LLVMLabel()
    def __repr__(self):
        return "%s %s" % (str(self.type), str(self.name))

LLVMFALSE = ConstLLVM(0, LLVMBOOLTYPE)
LLVMTRUE  = ConstLLVM(1, LLVMBOOLTYPE)

def getType(arg):
    if(isinstance(arg, ConstLLVM)):
        return arg.type
    elif(isinstance(arg, VarLLVM)):
        return arg.type
    elif(isinstance(arg, LabelArgLLVM)):
        return arg.type
    else:
        raise Exception("Attempting to get type of invalid argument: " + str(arg))

def setType(arg, _type):
    if(isinstance(arg, ConstLLVM)):
        arg.type = _type
    elif(isinstance(arg, VarLLVM)):
        arg.type = _type
    elif(isinstance(arg, LabelArgLLVM)):
        arg.type = _type
    else:
        raise Exception("Attempting to set type of invalid argument: " + str(arg))

def getArg(arg):
    if(isinstance(arg, ConstLLVM)):
        return arg.value
    elif(isinstance(arg, VarLLVM)):
        return arg.name
    elif(isinstance(arg, LabelArgLLVM)):
        return arg.name
    else:
        raise Exception("Attempting to get name of invalid argument: " + str(arg))

def setArg(arg, val):
    if(isinstance(arg, ConstLLVM)):
        arg.value = val
    elif(isinstance(arg, VarLLVM)):
        arg.name = val
    elif(isinstance(arg, LabelArgLLVM)):
        arg.name = val
    else:
        raise Exception("Attempting to set type of invalid argument: " + str(arg))

# LLVM Compound Args

class PhiPairLLVM(LLVMArg):
    def __init__(self, val, label):
        self.val   = val
        self.label = label
    def __repr__(self):
        return "[ %s, %s ]" % (str(getArg(self.val)), str(getArg(self.label)))

class SwitchPairLLVM(LLVMArg):
    def __init__(self, val, label):
        self.val   = val
        self.label = label
    def __repr__(self):
        return " %s, %s " % (str(self.val), str(self.label))

# LLVM Instructions

class LLVMInst(object):
    def __init__():
        pass

# Block Instructions

class BlockLLVMInst(LLVMInst):
    def __init__():
        pass


class defineLLVM(BlockLLVMInst):
    def __init__(self, _type, name, args, blocks):
        self.type = _type
        self.name = name
        self.args = args
        self.blocks = blocks
    def __repr__(self):
        return ("define %s %s(%s) {\n\t%s\n}" % (str(self.type),
                                                 str(self.name),
                                                 ", ".join(map(lambda x: str(x),
                                                               self.args)),
                                                 '\n\t'.join(map(lambda x: str(x),
                                                                 self.blocks))))

class blockLLVM(BlockLLVMInst):
    def __init__(self, label, instrs):
        self.label  = label
        self.instrs = instrs
    def __repr__(self):
        return "%s:\n\t\t%s\n" % (str(getArg(self.label).name),
                              '\n\t\t'.join(map(lambda x: str(x),
                                                self.instrs)))

# Terminator Instructions

class TermLLVMInst(LLVMInst):
    def __init__():
        pass

class retLLVM(TermLLVMInst):
    def __init__(self, value=None):
        self.value = value
    def __repr__(self):
        if(self.value == None):
            return ("ret void")
        else:
            return ("ret %s %s") % (str(getType(self.value)),
                                    str(getArg(self.value)))

class switchLLVM(TermLLVMInst):
    def __init__(self, value, defaultDest, altDests):
        self.value = value
        self.defaultDest = defaultDest
        self.altDests = altDests
    def __repr__(self):
        return ("switch %s %s, %s [ %s ]") % (str(getType(self.value)),
                                              str(getArg(self.value)),
                                              str(self.defaultDest),
                                              ' '.join(map(lambda x: str(x),
                                                           self.altDests)))

# Binary Instructions

class BinaryLLVMInst(LLVMInst):
    def __init__(self, target, left, right):
        if(getType(target) == getType(left) == getType(right)):
            self.type = getType(target)
        else:
            raise Exception("Binary instruction requires uniform type")
        self.target = target
        self.left = left
        self.right = right
    def emit(self, name):
        return ("%s = %s %s %s, %s" % (str(getArg(self.target)),
                                       str(name),
                                       str(self.type),
                                       str(getArg(self.left)),
                                       str(getArg(self.right)))) 

class addLLVM(BinaryLLVMInst):
    def __init__(self, *args, **kwargs):
        super(addLLVM, self).__init__(*args, **kwargs)
    def __repr__(self):
        return super(addLLVM, self).emit("add")

class subLLVM(BinaryLLVMInst):
    def __init__(self, *args, **kwargs):
        super(subLLVM, self).__init__(*args, **kwargs)
    def __repr__(self):
        return super(subLLVM, self).emit("sub")

# Conversion Instructions

class ConversionLLVMInst(LLVMInst):
    def __init__(self, target, value, outType):
        self.target  = target
        self.value   = value
        self.outType = outType
    def emit(self, name):
        return ("%s = %s %s %s to %s" % (str(getArg(self.target)),
                                         str(name),
                                         str(getType(self.value)),
                                         str(getArg(self.value)),
                                         str(self.outType))) 

class zextLLVM(ConversionLLVMInst):
    def __init__(self, *args, **kwargs):
        super(zextLLVM, self).__init__(*args, **kwargs)
    def __repr__(self):
        return super(zextLLVM, self).emit("zext")

class sextLLVM(ConversionLLVMInst):
    def __init__(self, *args, **kwargs):
        super(sextLLVM, self).__init__(*args, **kwargs)
    def __repr__(self):
        return super(sextLLVM, self).emit("sext")

class ptrtointLLVM(ConversionLLVMInst):
    def __init__(self, *args, **kwargs):
        super(ptrtointLLVM, self).__init__(*args, **kwargs)
    def __repr__(self):
        return super(ptrtointLLVM, self).emit("ptrtoint")

class inttoptrLLVM(ConversionLLVMInst):
    def __init__(self, *args, **kwargs):
        super(inttoptrLLVM, self).__init__(*args, **kwargs)
    def __repr__(self):
        return super(inttoptrLLVM, self).emit("inttoptr")

# Other Instructions

class OtherLLVMInst(LLVMInst):
    def __init__():
        pass

class declareLLVMString(OtherLLVMInst):
    def __init__(self, target, _str):
        self.string = _str
        self.target = target
    def __repr__(self):
        return ("%s = private unnamed_addr constant %s" % (str(self.target.name), str(self.string)))

class getelementptrLLVM(OtherLLVMInst):
    # %cast210 = getelementptr [13 x i8]* @.str, i64 0, i64 0
    # <result> = getelementptr <pty>* <ptrval>{, <ty> <idx>}*
    def __init__(self, target, pointedTo, args):
        self.ptdTo = pointedTo
        self.target = target
        self.args = args
    def __repr__(self):
        return "%s = getelementptr %s* %s, %s" % (str(getArg(self.target)),
                                                  str(self.ptdTo.type),
                                                  str(self.ptdTo.name),
                                                  ", ".join(map(lambda x: str(x),
                                                                self.args)))

class icmpLLVM(OtherLLVMInst):
    def __init__(self, target, op, left, right):
        if(getType(left) == getType(right)):
            self.argType = getType(left)
        else:
            raise Exception("icmp instruction requires uniform arg types")
        self.target = target
        self.op = op
        self.left = left
        self.right = right
    def __repr__(self):
        return ("%s = icmp %s %s %s, %s" % (str(getArg(self.target)),
                                            str(self.op),
                                            str(self.argType),
                                            str(getArg(self.left)),
                                            str(getArg(self.right))))

class callLLVM(OtherLLVMInst):
    def __init__(self, _type, name, args, target=None):
        self.type = _type
        self.name = name
        self.args = args
        self.target = target
    def __repr__(self):
        string = ("call %s %s(%s)") % (str(self.type),
                                       str(self.name),
                                       ", ".join(map(lambda x: str(x),
                                                     self.args)))
        if(self.target == None):
            return string
        else:
            return "%s = %s" % (str(getArg(self.target)), string)

class phiLLVM(OtherLLVMInst):
    def __init__(self, target, pairs):
        _type = None
        for pair in pairs:
            if(_type == None):
                _type = getType(pair.val)
            else:
                if(_type != getType(pair.val)):
                    raise Exception("phi instruction requires uniform val types")
        self.type   = _type
        self.target = target
        self.pairs  = pairs
    def __repr__(self):
        return "%s = phi %s %s" % (str(getArg(self.target)),
                                   str(self.type),
                                   ", ".join(map(lambda x: str(x), self.pairs)))
