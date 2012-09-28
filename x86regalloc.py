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

    def validNode(val):
        return isinstance(val, Var86)

    def name(val):
        if isinstance(val, Var86):
            return val.name
        else:
            raise Exception("Attempting to get name of invalid argument: " + str(val))

    def extractVars(instr):
        written = []
        read = []
        
        # Unary read/write
        if(isinstance(instr, Neg86)):
            if(validNode(instr.target)):
                written += [name(instr.target)]
                read    += [name(instr.target)]
        
        # Unary read
        if(isinstance(instr, Push86)):
            if(validNode(instr.value)):
                read    += [name(instr.value)]
        
        # Binary read + read/write
        elif(isinstance(instr, Add86) or
             isinstance(instr, Sub86)):
            if(validNode(instr.target)):
                written += [name(instr.target)]
                read    += [name(instr.target)]
            if(validNode(instr.value)):
                read    += [name(instr.value)]
        
        # Binary read + write
        elif(isinstance(instr, Move86)):
            if(validNode(instr.target)):
                written += [name(instr.target)]
            if(validNode(instr.value)):
                read    += [name(instr.value)]
        
        # Return
        return instrVars(set(written), set(read))
        
    # Copy and reverse instruction list
    rinstrs = instrs[:]
    rinstrs.reverse()

    # Iterate through list and build lafter
    lafter = [set([])]
    for n in rinstrs:
        instrvars = extractVars(n)
        lafter += [(lafter[-1] - instrvars.written) | instrvars.read]

    # Reverse and return lafter
    lafter.reverse()
    return lafter[1:]

def interference(instrs, lafter):
    # Add callee save register to seed graph
    # graph = {'eax' : set([]), 'ecx' : set([]), 'edx' : set([])}
    graph = {}

    def validNode(val):
        return isinstance(val, Var86)

    def name(val):
        if isinstance(val, Var86):
            return val.name
        else: raise Exception("Attempting to get name of invalid argument: " + str(val))

    def addEdge(x, y):
        graph[x].add(y)
        graph[y].add(x)
    
    def addKey(instr):
        if(isinstance(instr, Move86) or
           isinstance(instr, Add86) or
           isinstance(instr, Sub86)):
            if(validNode(instr.value)):
                graph[name(instr.value)] = set([])
            if(validNode(instr.target)):
                graph[name(instr.target)] = set([])
        if(isinstance(instr, Push86)):
            if(validNode(instr.value)):
                graph[name(instr.value)] = set([])
        if(isinstance(instr, Neg86)):
            if(validNode(instr.target)):
                graph[name(instr.target)] = set([])

    def updateGraph(instr, live):
        # If 'move' instruction
        if(isinstance(instr, Move86)):
            if(validNode(instr.target)):
                t = name(instr.target)
                # If t is in live set
                if(t in live):
                    # Loop through set
                    for v in live:
                        # Add edge unless v=t or v=s
                        if(v != t):
                            if(validNode(instr.value)):
                                s = name(instr.value)
                                if(v != s):
                                    addEdge(t, v)
                            else:
                                addEdge(t, v)
        # If arithmetic
        elif(isinstance(instr, Add86) or
             isinstance(instr, Sub86) or 
             isinstance(instr, Neg86)):
            if(validNode(instr.target)):
                t = name(instr.target)
                # If t is in live set
                if(t in live):
                    # Loop through set
                    for v in live:
                        # Add edge unless v=t
                        if(v != t):
                            addEdge(t, v)
                            

    if(len(instrs) != len(lafter)):
        raise Exception("Mismatched lenghts")

    # Seed Graph
    for instr in instrs:
        addKey(instr)

    for n in range(len(instrs)):
        print str(instrs[n]) + " " + str(lafter[n])
        updateGraph(instrs[n], lafter[n])

    return graph
