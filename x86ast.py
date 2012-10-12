"""Mike's x86 AST tree nodes"""

class X86Arg:
    def __str__(self):
        return self.mnemonic()
    def __repr__(self):
        return self.mnemonic()
    def __hash__(self):
        return hash(self.__str__())
    def __eq__(self, that):
        return self.mnemonic() == that.mnemonic()
    
class Const86(X86Arg):
    def __init__(self, value):
        self.value = value
    def mnemonic(self):
        return '$' + str(self.value)

class Reg86(X86Arg):
    def __init__(self, register):
        self.register = register
    def mnemonic(self):
        return '%' + self.register

class Mem86(X86Arg):
    def __init__(self, offset, arg):
        self.offset = offset
        self.arg = arg
    def mnemonic(self):
        return ('-%d(%s)' % (self.offset, self.arg.mnemonic()))

class Var86(X86Arg):
    def __init__(self, name):
        self.name = name
    def mnemonic(self):
        return self.name

EAX = Reg86('eax')
EBX = Reg86('ebx')
ECX = Reg86('ecx')
EDX = Reg86('edx')
ESI = Reg86('esi')
EDI = Reg86('edi')
EBP = Reg86('ebp')
ESP = Reg86('esp')

CALLEESAVE = [EAX, ECX, EDX]
COLOREDREGS = [EAX, EBX, ECX, EDX, ESI, EDI]

class X86Inst:
    def __str__(self):
        return self.mnemonic()
    def __repr__(self):
        return self.mnemonic()

class Push86(X86Inst):
    def __init__(self, value):
        self.value = value
    def mnemonic(self):
        return 'pushl ' + self.value.mnemonic() 

class Move86(X86Inst):
    def __init__(self, value, target):
        self.value = value
        self.target = target
    def mnemonic(self):
        return ('movl %s, %s' % (self.value.mnemonic(), self.target.mnemonic()))

class Sub86(X86Inst):
    def __init__(self, value, target):
        self.value = value
        self.target = target
    def mnemonic(self):
        return ('subl %s, %s' % (self.value.mnemonic(), self.target.mnemonic()))

class Add86(X86Inst):
    def __init__(self, value, target):
        self.value = value
        self.target = target
    def mnemonic(self):
        return ('addl %s, %s' % (self.value.mnemonic(), self.target.mnemonic()))

class Neg86(X86Inst):
    def __init__(self, target):
        self.target = target
    def mnemonic(self):
        return 'negl ' + self.target.mnemonic()

class Call86(X86Inst):
    def __init__(self, function):
        self.function = function
    def mnemonic(self):
        return 'call ' + self.function

class Leave86(X86Inst):
    def mnemonic(self):
        return 'leave'

class Ret86(X86Inst):
    def mnemonic(self):
        return 'ret'
