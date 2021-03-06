# CU CS5525
# Fall 2012
# GSV Python Compiler
#
# x86ast.py
# x86 Instruction AST Nodes
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

# x86 Constants and Aliases
X86_EQ = "sete"
X86_NE = "setne"
X86_GT = "setg"
X86_GE = "setge"
X86_LT = "setl"
X86_LE = "setle"

import sys

"""x86 AST tree nodes"""

class X86Arg:
    def __str__(self):
        return self.mnemonic()
    def __repr__(self):
        return self.mnemonic()
    def __hash__(self):
        return hash(self.__repr__())
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
        return ('%d(%s)' % (self.offset, self.arg.mnemonic()))

class Var86(X86Arg):
    def __init__(self, name):
        self.name = name
    def mnemonic(self):
        return self.name

class IndirectJumpLabel86(X86Arg):
    def __init__(self, name):
        self.name = name
    def mnemonic(self):
        return '$' + ('_' if sys.platform == 'darwin' else '') + self.name

EAX = Reg86('eax')
EBX = Reg86('ebx')
ECX = Reg86('ecx')
EDX = Reg86('edx')
ESI = Reg86('esi')
EDI = Reg86('edi')
EBP = Reg86('ebp')
ESP = Reg86('esp')

AL = Reg86('al')
AH = Reg86('ah')
AX = Reg86('ax')
BL = Reg86('bl')
BH = Reg86('bh')
BX = Reg86('bx')
CL = Reg86('cl')
CH = Reg86('ch')
CX = Reg86('cx')
DL = Reg86('dl')
DH = Reg86('dh')
DX = Reg86('dx')

CALLERSAVE  = [EAX, ECX, EDX]
CALLEESAVE  = [EBX, ESI, EDI]
COLOREDREGS = [EAX, EBX, ECX, EDX, ESI, EDI]
STRINGREGS  = [ESI, EDI]

ONEBYTELOWREGS = {EAX: AL, EBX: BL, ECX: CL, EDX: DL}
ONEBYTEHIREGS  = {EAX: AH, EBX: BH, ECX: CH, EDX: DH}
TWOBYTEREGS    = {EAX: AX, EBX: BX, ECX: CX, EDX: DX}

WORDLEN    = 4 #Bytes
STACKALIGN = 4 #Words

x86ZERO  = Const86(0)
x86ONE   = Const86(1)

x86FALSE = x86ZERO
x86TRUE  = x86ONE

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

class Pop86(X86Inst):
    def __init__(self, value):
        self.value = value
    def mnemonic(self):
        return 'popl ' + self.value.mnemonic() 

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

class Not86(X86Inst):
    def __init__(self, target):
        self.target = target
    def mnemonic(self):
        return 'notl ' + self.target.mnemonic()

class Call86(X86Inst):
    def __init__(self, function):
        self.function = function
    def mnemonic(self):
        if(sys.platform == 'darwin'):
            instrStr = 'call _%s' % self.function
        else:
            instrStr = 'call %s' % self.function
        return instrStr

class IndirectCall86(X86Inst):
    def __init__(self, function):
        self.function = function
    def mnemonic(self):
        return 'call *' + self.function.mnemonic()

class LShift86(X86Inst):
    def __init__(self, value, target):
        self.value = value
        self.target = target
    def mnemonic(self):
        return ('sall %s, %s' % (self.value.mnemonic(), self.target.mnemonic()))

class RShift86(X86Inst):
    def __init__(self, value, target):
        self.value = value
        self.target = target
    def mnemonic(self):
        return ('sarl %s, %s' % (self.value.mnemonic(), self.target.mnemonic()))    

class Or86(X86Inst):
    def __init__(self, value, target):
        self.value = value
        self.target = target
    def mnemonic(self):
        return ('orl %s, %s' % (self.value.mnemonic(), self.target.mnemonic()))

class And86(X86Inst):
    def __init__(self, value, target):
        self.value = value
        self.target = target
    def mnemonic(self):
        return ('andl %s, %s' % (self.value.mnemonic(), self.target.mnemonic()))

class Comp86(X86Inst):
    def __init__(self, value, target):
        self.value = value
        self.target = target
    def mnemonic(self):
        return ('cmpl %s, %s' % (self.value.mnemonic(), self.target.mnemonic()))

class SetCmp86(X86Inst):
    def __init__(self, op, target):
        self.op     = op
        self.target = target
    def mnemonic(self):
        return ('%s %s' % (self.op, self.target.mnemonic()))

class Jump86(X86Inst):
    def __init__(self, target):
        self.target = target
    def mnemonic(self):
        return ('jmp %s' % self.target)

class JumpEqual86(X86Inst):
    def __init__(self, target):
        self.target = target
    def mnemonic(self):
        return ('je %s' % self.target)

class Label86(X86Inst):
    def __init__(self, name):
        self.name = name
    def mnemonic(self):
        return self.name + ':'

class If86(X86Inst):
    def __init__(self, then, else_):
        self.then = then
        self.else_ = else_
    def mnemonic(self):
        return ('\n\t'.join(map(lambda x: x.mnemonic(), self.then)) +
                '\n\t' + '\n\t'.join(map(lambda x: x.mnemonic(), self.else_)))
    
class Leave86(X86Inst):
    def mnemonic(self):
        return 'leave'

class Ret86(X86Inst):
    def mnemonic(self):
        return 'ret'

class Func86(X86Inst):
    def __init__(self, name, nodes):
        self.name = name
        self.nodes = nodes
    def mnemonic(self):
        name = self.name if sys.platform != 'darwin' else ('_' + self.name)
        return '.globl %s\n%s:\n\t%s\n' % (name,
                                           name,
                                           '\n\t'.join(map(lambda x: x.mnemonic(), self.nodes)))

class Loop86(X86Inst):
    def __init__(self, test, body):
        self.test = test
        self.body = body
    def mnemonic(self):
        return ('\n\t'.join(map(lambda x: x.mnemonic(), self.test)) +
                '\n\t' + '\n\t'.join(map(lambda x: x.mnemonic(), self.body)))

class String86(X86Inst):
    def __init__(self, location, name):
        self.location = location
        self.name = name
    def mnemonic(self):
        return '%s:\n\t.asciz \"%s\"' % (self.location, self.name)
