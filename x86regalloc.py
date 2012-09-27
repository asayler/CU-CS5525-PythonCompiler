from x86ast import *

EAX = Reg86('eax')
EBX = Reg86('ebx')
ECX = Reg86('ecx')
EDX = Reg86('edx')
ESI = Reg86('esi')
EDI = Reg86('edi')
EBP = Reg86('ebp')
ESP = Reg86('esp')



def liveness(instrs):
    class instrVars:
        def __init__(self, written, read):
            self.written = written
            self.read = read
        def __str__(self):
            return "w:" + str(self.written) + " r:" + str(self.read)

    def extractVars(instr):
        written = []
        read = []
        
        # Unary read/write
        if(isinstance(instr, Neg86)):
            if(isinstance(instr.target, Var86)):
                written += instr.target.name
                read    += instr.target.name
        
        # Unary read
        if(isinstance(instr, Push86)):
            if(isinstance(instr.target, Var86)):
                written += instr.target.name
                read    += instr.target.name
        
        # Binary read + read/write
        elif(isinstance(instr, Add86) or
             isinstance(instr, Sub86)):
            if(isinstance(instr.target, Var86)):
                written += instr.target.name
                read    += instr.target.name
            if(isinstance(instr.value, Var86)):
                read    += instr.value.name
        
        # Binary read + write
        elif(isinstance(instr, Move86)):
            if(isinstance(instr.target, Var86)):
                written += instr.target.name
            if(isinstance(instr.value, Var86)):
                read    += instr.value.name
                    
        return instrVars(set(written), set(read))
        
    # Copy and reverse instruction list
    rinstrs = instrs[:]
    rinstrs.reverse()

    # Iternate through list and build lafter
    lafter = [set([])]
    for n in rinstrs:
        instrvars = extractVars(n)
        lafter += [(lafter[-1] - instrvars.written) | instrvars.read]

    # Reverse and return lafter
    lafter.reverse()
    return lafter
