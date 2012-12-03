# CU CS5525
# Fall 2012
# Python Compiler
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
#    Andy Sayler
#       http://www.andysayler.com
#    Michael (Mike) Vitousek
#       http://csel.cs.colorado.edu/~mivi2269/

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

I1   = LLVMInt(1)
I8   = LLVMInt(8)
I32  = LLVMInt(32)
I64  = LLVMInt(64)
PI32 = LLVMPointer(I8)
PI32 = LLVMPointer(I32)
PI64 = LLVMPointer(I64)

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

LLVMZERO  = ConstLLVM(0, I32)
LLVMONE   = ConstLLVM(1, I32)
LLVMFALSE = ConstLLVM(0, I1)
LLVMTRUE  = ConstLLVM(1, I1)

def getType(arg):
    if(isinstance(arg, ConstLLVM)):
        return arg.type
    elif(isinstance(arg, VarLLVM)):
        return arg.type
    elif(isinstance(arg, LabelArgLLVM)):
        return arg.type
    else:
        raise Exception("Attempting to get type of invalid argument: " + str(arg))

def getArg(arg):
    if(isinstance(arg, ConstLLVM)):
        return arg.value
    elif(isinstance(arg, VarLLVM)):
        return arg.name
    elif(isinstance(arg, LabelArgLLVM)):
        return arg.name
    else:
        raise Exception("Attempting to get name of invalid argument: " + str(arg))

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
        return "%s:\n\t\t%s" % (str(getArg(self.label).name),
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
                                       str(self._type),
                                       str(getArg(self.left)),
                                       str(getArg(self.right)))) 

class addLLVM(BinaryLLVMInst):
    def __init__(self, *args, **kwargs):
        super(addLLVM, self).__init__(*args, **kwargs)
    def __repr__(self):
        return super(addLLVM, self).emit("add")

class subLLVM(BinaryLLVMInst):
    def __init__(self, *args, **kwargs):
        super(addLLVM, self).__init__(*args, **kwargs)
    def __repr__(self):
        return super(addLLVM, self).emit("sub")

# Other Instructions

class OtherLLVMInst(LLVMInst):
    def __init__():
        pass

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
        return ("%s = icmp %s %s %s, %s)" % (str(getArg(self.target)),
                                             str(self.op),
                                             str(self.argType),
                                             set(getArg(self.left)),
                                             set(getArg(self.right))))

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
