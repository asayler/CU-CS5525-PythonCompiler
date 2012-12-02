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

# LLVM Args

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

LLVMZERO  = ConstLLVM(0, I32)
LLVMONE   = ConstLLVM(1, I32)

def getType(arg):
    if(isinstance(arg, ConstLLVM)):
        return arg.type
    if(isinstance(arg, VarLLVM)):
        return arg.type
    else:
        raise Exception("Attempting to get type of invalid argument: " + str(arg))

def getArg(arg):
    if(isinstance(arg, ConstLLVM)):
        return arg.value
    if(isinstance(arg, VarLLVM)):
        return arg.name
    else:
        raise Exception("Attempting to get name of invalid argument: " + str(arg))

# LLVM Instructions

class LLVMInst(object):
    def __init__():
        pass

# Block Instructions

class BlockLLVMInst(LLVMInst):
    def __init__():
        pass

class DefineLLVM(BlockLLVMInst):
    def __init__(self, _type, name, args, instrs):
        self.type = _type
        self.name = name
        self.args = args
        self.instrs = instrs
    def __repr__(self):
        return ("define %s %s(%s) {\n\t%s\n}" % (str(self.type),
                                                 str(self.name),
                                                 ", ".join(map(lambda x: str(x),
                                                               self.args)),
                                                 '\n\t'.join(map(lambda x: str(x),
                                                                 self.instrs))))

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

# Binary Instructions

class BinaryLLVMInst(LLVMInst):
    def __init__(self, target, left, right):
        if(target.type == left.type == right.type):
            self.type = target.type
        else:
            raise Exception("Binary instruction requires uniform type")
        self.target = target
        self.left = left
        self.right = right
    def emit(name):
        return ("%s = %s %s %s, %s" % (str(getArg(target)),
                                       str(name),
                                       str(_type),
                                       str(getArg(left)),
                                       str(getArg(right)))) 

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
