# Andy Sayler
# Fall 2012
# CU CS5525
# Python Compiler
# Reg Alloc Module
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

import sys

from x86ast import *

debug = True

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
            raise Exception("Attempting to get name of invalid argument: " +
                            str(val))

    def extractVars(instr):
        written = []
        read = []
        
        # Unary read/write
        if(isinstance(instr, Neg86)):
            if(validNode(instr.target)):
                written += [name(instr.target)]
                read    += [name(instr.target)]
        
        # Unary read
        elif(isinstance(instr, Push86)):
            if(validNode(instr.value)):
                read    += [name(instr.value)]
        
        # Binary read + read
        elif(isinstance(instr, Comp86)):
            if(validNode(instr.left)):
                read    += [name(instr.left)]
            if(validNode(instr.right)):
                read    += [name(instr.right)]

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

        # No Action
        elif(isinstance(instr, Call86),
             isinstance(instr, Jump86),
             isinstance(instr, JumpEqual86),
             isinstance(instr, Label86)):
            pass

        # Unhandled Error
        else:
            raise Exception("regalloc: Un-handled Node liveness")
        
        # Return
        return instrVars(set(written), set(read))

    def livenessSeq(instrseq, lafterbranch=set([])):
        
        # Copy and reverse instruction list
        rinstrs = instrseq[:]
        rinstrs.reverse()
        instrs = []

        # Iterate through list and build lafter
        lafter = [lafterbranch]
        for n in rinstrs:
            if(isinstance(n, If86)):
                # Branching Instruction
                # Pop last item for passing to recursive call
                previous = lafter.pop()
                # Else Sequence
                lafterelse, instrselse = livenessSeq(n.else_, previous)
                instrselse.reverse()
                lafterelse.reverse()
                instrs += instrselse
                lafter += lafterelse
                # Then Sequence
                lafterthen, instrsthen = livenessSeq(n.then, previous)
                instrsthen.reverse()
                lafterthen.reverse()
                instrs += instrsthen
                lafter += lafterthen
                # Replace last item with union of last item output from lafters recursive calls
                lafter += [lafterelse[-1] | lafterthen[-1]]
            else:
                # Normal Instruction
                instrs += [n]
                instrvars = extractVars(n)
                lafter += [(lafter[-1] - instrvars.written) | instrvars.read]
           
        # Reverse and return lafter
        instrs.reverse()
        lafter.reverse()
        return (lafter[1:], instrs)

    return livenessSeq(instrs);

def interference(instrs, lafter):
    #Setup Empty Graph
    graph = {}
    
    def validNode(val):
        return (isinstance(val, Var86) or (isinstance(val, Reg86) and (val in COLOREDREGS)))

    def name(val):
        if(isinstance(val, Var86)):
            return val.name
        elif(isinstance(val, Reg86)):
            return val.register
        else:
            raise Exception("regalloc: Attempting to get name of invalid argument: " + str(val))

    def addEdge(x, y):
        graph[x].add(y)
        graph[y].add(x)
    
    def addKey(instr):

        # value+target nodes
        if(isinstance(instr, Move86) or
           isinstance(instr, Add86) or
           isinstance(instr, Sub86)):
            if(validNode(instr.value)):
                graph[name(instr.value)] = set([])
            if(validNode(instr.target)):
                graph[name(instr.target)] = set([])
        
        # value only nodes
        elif(isinstance(instr, Push86)):
            if(validNode(instr.value)):
                graph[name(instr.value)] = set([])
        
        # target only nodes
        elif(isinstance(instr, Neg86)):
            if(validNode(instr.target)):
                graph[name(instr.target)] = set([])

        # left right nodes
        elif(isinstance(instr, Comp86)):
            if(validNode(instr.left)):
                graph[name(instr.left)] = set([])
            if(validNode(instr.right)):
                graph[name(instr.right)] = set([])

        # No Action for non-register instructions
        elif(isinstance(instr, Jump86),
             isinstance(instr, JumpEqual86),
             isinstance(instr, Label86),
             isinstance(instr, Call86)):
            pass

        # No Key Nodes
        else:
            raise Exception("regalloc: Attempting to addkey for invalid instr " + str(instr))

    def updateGraph(instr, live):

        # If 'move' instruction
        if(isinstance(instr, Move86)):
            if(validNode(instr.target)):
                t = name(instr.target)
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

        
        # No Action for read only and non-register instructions
        elif(isinstance(instr, Jump86),
             isinstance(instr, JumpEqual86),
             isinstance(instr, Label86),
             isinstance(instr, Comp86),
             isinstance(instr, Push86)):
            pass

        # Unhandled Error
        else:
            raise Exception("regalloc: Un-handled Node %s" % str(instr))

    # Check Length
    if(len(instrs) != len(lafter)):
        raise Exception("Mismatched lengths")

    # Seed Graph
    for reg in CALLEESAVE:
        if(validNode(reg)):
            graph[name(reg)] = set([])
    for instr in instrs:
        addKey(instr)

    # Add edges
    for n in range(len(instrs)):
        updateGraph(instrs[n], lafter[n])

    return graph

def color(graph, colors = {}, regOnlyVars = []):

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
    
    # Clear Register Assignments from Previous Passes
    assigned = filter(lambda u: ((colors[u] != None) and
                                 (not(u in REGCOLORS))), colors.keys())
    for key in assigned:
        if(colors[key] < len(REGCOLORS)):
            colors[key] = None
            
    # Find all uncolord keys
    w = filter(lambda u: colors[u] == None, colors.keys())
    
    while(len(w) > 0):
        
        # Find regOnlyKeys in Keys
        priorityKeys = []
        for key in w:
            if(key in regOnlyVars):
               priorityKeys += [key]
        # Else use all keys
        if(len(priorityKeys) == 0):
            priorityKeys = w
        
        # Find key with max saturation
        maxkeys = []
        maxsat = -1
        for key in priorityKeys:
            sat = saturation(key)
            if(sat > maxsat):
                maxsat = sat
                maxkeys = [key]
            elif(sat == maxsat):
                maxkeys += [key]
        # Break ties
        # Nothing to break currently
        # Otherwise use first var
        maxkey = maxkeys[0]
        
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

        # Double check reg only var assignment
        if(maxkey in regOnlyVars):
            if(colors[maxkey] >= len(REGCOLORS)):
                raise Exception("Failed to place regOnlyVar in reg: " +
                                str(maxkey) + "," + str(colors[maxkey]))

    return colors

def fixMemToMem(instrs, colors):

    regTempPrefix = "RegTmp"

    def validNode(val):
        return isinstance(val, Var86)

    def name(val):
        if isinstance(val, Var86):
            return val.name
        else:
            raise Exception("Attempting to get name of invalid argument: " + str(val))

    def addTemp(instr, tmp):
        if(isinstance(instr, Add86)):
            return [Move86(instr.value, tmp),
                    Add86(tmp, instr.target)]
        elif(isinstance(instr, Sub86)):
            return [Move86(instr.value, tmp),
                    Sub86(tmp, instr.target)]
        elif(isinstance(instr, Move86)):
            return [Move86(instr.value, tmp),
                    Move86(tmp, instr.target)]
        else:
            raise Exception("Cannot add temp to node: " + str(instr))
    
    tempCnt = 0
    fixedInstrs = []
    regOnlyVars = []

    #Loop through instructions
    for instr in instrs:
        
        # Binary read/write
        if(isinstance(instr, Add86) or
           isinstance(instr, Sub86) or
           isinstance(instr, Move86)):
            if(validNode(instr.target) and 
               validNode(instr.value)):
                # Find mem to mem operations
                if((colors[name(instr.target)] >= len(REGCOLORS)) and
                   (colors[name(instr.value)] >= len(REGCOLORS))):
                    # Add temp var
                    tmp = Var86(regTempPrefix + str(tempCnt))
                    fixedInstrs += addTemp(instr, tmp)
                    regOnlyVars += [tmp.name]
                    tempCnt += 1
                else:
                    fixedInstrs += [instr]
            else:
                fixedInstrs += [instr]
        else:
            fixedInstrs += [instr]

    return (fixedInstrs, regOnlyVars)

def varReplace(instrs, colors):

    def validNode(val):
        return isinstance(val, Var86)

    def name(val):
        if isinstance(val, Var86):
            return val.name
        else:
            raise Exception("Attempting to get name of invalid argument: " + str(val))

    def replace(node, colormap):
        color = colors[name(node)]
        if(color < len(REGCOLORS)):
            # Set Register
            return Reg86(colormap[color])
        else:
            # Set stack spill
            return Mem86((color - len(REGCOLORS) + 1) * WORDLEN, EBP)

    #Duplicate
    instrs = instrs[:]

    #Setup reverse dictionary
    colormap = {}
    for key in REGCOLORS:
        colormap[REGCOLORS[key]] = key

    #Loop through instructions
    for instr in instrs:

        # Unary read/write
        if(isinstance(instr, Neg86)):
            if(validNode(instr.target)):
                instr.target = replace(instr.target, colormap)
            
        # Unary read
        elif(isinstance(instr, Push86)):
            if(validNode(instr.value)):
                instr.value = replace(instr.value, colormap)
        
        # Binary read/write
        elif(isinstance(instr, Add86) or
             isinstance(instr, Sub86) or
             isinstance(instr, Move86)):
            if(validNode(instr.target)):
                instr.target = replace(instr.target, colormap)
            if(validNode(instr.value)):
                instr.value = replace(instr.value, colormap)

        # Binary read/read
        elif(isinstance(instr, Comp86)):
            if(validNode(instr.left)):
                instr.left = replace(instr.left, colormap)
            if(validNode(instr.right)):
                instr.right = replace(instr.right, colormap)

        # No Action
        elif(isinstance(instr, Call86),
             isinstance(instr, Jump86),
             isinstance(instr, JumpEqual86),
             isinstance(instr, Label86)):
            pass
        
        # Unhandled Error
        else:
            raise Exception("regalloc: Un-handled Node during var replace")

    return instrs

def maxColor(colors):
    maxcolor = -1
    for key in colors:
        color = colors[key]
        if(color > maxcolor):
            maxcolor = color
    return maxcolor

def addPreamble(instrs, colors):
    stackvars = maxColor(colors) - len(REGCOLORS) + 1
    preamble = [Push86(EBP),
                Move86(ESP, EBP)]
    if(stackvars > 0):
        preamble += [Sub86(Const86(stackvars * WORDLEN), ESP)]
    return preamble + instrs

def addClosing(instrs):
    closing = [Move86(Const86(0), EAX),
               Leave86(),
               Ret86()]
    return instrs + closing

def regAlloc(instrs):
    
    (lafter, instrseq) = liveness(instrs)
    if(debug):
        sys.stderr.write("lafter      =\n" + "\n".join(map(str, lafter)) + "\n")
        sys.stderr.write("instrseq    =\n" + "\n".join(map(str, instrseq)) + "\n")
    graph = interference(instrseq, lafter)
    if(debug):
        sys.stderr.write("graph       =\n" + str(graph) + "\n")
    colors = color(graph)
    if(debug):
        sys.stderr.write("colors      =\n" + str(colors) + "\n")
    (instrseq, regOnlyVars) = fixMemToMem(instrseq, colors)
    if(debug):
        sys.stderr.write("instrseq    =\n" + "\n".join(map(str, instrseq)) + "\n")
        sys.stderr.write("regOnlyVars =\n" + str(regOnlyVars) + "\n")
    lafter, instrseq = liveness(instrseq)
    graph = interference(instrseq, lafter)
    colors = color(graph, colors, regOnlyVars)
    instrseq = varReplace(instrseq, colors)
    instrseq = addPreamble(instrseq, colors)
    instrseq = addClosing(instrseq)

    return instrseq
