from x86ast import *

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

def regname(reg):
    if(isinstance(reg, Reg86)):
        return reg.register
    else:
        raise Exception("Attempting to get name of invalid argument: " + str(val))

REGCOLORS = {
    regname(EAX): 0,
    regname(EBX): 1,
    regname(ECX): 2,
    regname(EDX): 3,
    regname(ESI): 4,
    regname(EDI): 5
}

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
    #Setup Empty Graph
    graph = {}
    
    def validNode(val):
        return (isinstance(val, Var86) or
                (isinstance(val, Reg86) and (val in COLOREDREGS)))

    def name(val):
        if(isinstance(val, Var86)):
            return val.name
        elif(isinstance(val, Reg86)):
            return val.register
        else:
            raise Exception("Attempting to get name of invalid argument: " + str(val))

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
        # If call
        elif(isinstance(instr, Call86)):
            for v in live:
                # Add edge for each callee save register
                for reg in CALLEESAVE:
                    if(validNode(reg)):
                        r = name(reg)
                        if(v != r):
                            addEdge(r, v)                          

    # Check Length
    if(len(instrs) != len(lafter)):
        raise Exception("Mismatched lengths")

    # Seed Graph
    for reg in CALLEESAVE:
        if(validNode(reg)):
            graph[name(reg)] = set([])
    print graph
    for instr in instrs:
        addKey(instr)

    # Add edges
    for n in range(len(instrs)):
        updateGraph(instrs[n], lafter[n])

    return graph

def color(graph):

    colors = {}

    def saturation(key):
        sat = 0
        # Loop through neighbors
        for n in graph[key]:
            if(colors[n] != None):
                sat += 1
        return sat

    # Seed colors
    for key in graph.keys():
        if(not(key in colors)):
            if(key in REGCOLORS):
                colors[key] = REGCOLORS[key]
            else:
                colors[key] = None
    
    # Find all uncolord keys
    w = filter(lambda u: colors[u] == None, colors.keys())
    
    while(len(w) > 0):
        # Find key with max saturation
        maxkey = ''
        maxsat = -1
        for key in w:
            print(key + " sat = " + str(saturation(key)))
            sat = saturation(key)
            if(sat > maxsat):
                maxsat = sat
                maxkey = key
        # Select color for key with max saturation and remove from w
        adjcolors = set([])
        for n in graph[maxkey]:
            if(colors[n] != None):
                adjcolors.add(colors[n])
        color = 0
        while(1):
            if(color in adjcolors):
                color += 1
            else:
                colors[maxkey] = color
                w.remove(maxkey)
                break

    return colors

