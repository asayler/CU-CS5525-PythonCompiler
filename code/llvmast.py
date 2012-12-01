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
        return ('%s*' % (str(self.value)))    

I8   = LLVMInt(8)
I32  = LLVMInt(32)
I64  = LLVMInt(64)
PI32 = LLVMPointer(I8)
PI32 = LLVMPointer(I32)
PI64 = LLVMPointer(I64)

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
        return str(self.value)

class VarLLVM(LLVMArg):
    def __init__(self, name, _type):
        self.name = name
        self.type = _type
    def __repr__(self):
        return str(self.name)

LLVMZERO  = Const86(0, I32)
LLVMONE   = Const86(1, I32)

def getType(arg):
    if(isinstance(arg, ConstLLVM)):
        return arg.type
    if(isinstance(arg, VarLLVM)):
        return arg.type
    else:
        raise Excpetion("Attempting to get type of invalid argument: " + str(arg))

def getArg(arg):
    if(isinstance(arg, ConstLLVM)):
        return arg.value
    if(isinstance(arg, VarLLVM)):
        return arg.name
    else:
        raise Excpetion("Attempting to get name of invalid argument: " + str(arg))

# LLVM Instructions

class LLVMInst(object):
    def __init__():
        pass

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
