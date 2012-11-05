# CU CS5525
# Fall 2012
# Python Compiler
#
# x86regalloc.py
# Reg Alloc Module
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

import sys

from x86ast import *

from utilities import generate_name
from utilities import generate_return_label

debug = False

MAXITERATIONS = 9
MAXLOOPCNT = 3

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
        elif(isinstance(instr, IndirectCall86)):
            if(validNode(instr.function)):
                read    += [name(instr.function)]

        # Unary write
        elif(isinstance(instr, SetEq86) or
             isinstance(instr, SetNEq86)):
            if(validNode(instr.target)):
                written    += [name(instr.target)]

        # Binary read + read
        elif(isinstance(instr, Comp86)):
            if(validNode(instr.value)):
                read    += [name(instr.value)]
            if(validNode(instr.target)):
                read    += [name(instr.target)]

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
                livesetelse = lafterelse.pop()
                instrs += instrselse
                lafter += lafterelse
                # Then Sequence
                lafterthen, instrsthen = livenessSeq(n.then, previous)
                instrsthen.reverse()
                lafterthen.reverse()
                livesetthen = lafterthen.pop()
                instrs += instrsthen
                lafter += lafterthen
                # Replace last item with union of last item output from lafters recursive calls
                lafter += [livesetelse | livesetthen]
            elif(isinstance(n, Loop86)):
                # Loop Instruction
                loopcnt = 0
                while(True):
                    # Pop last item for passing to recursive call
                    previous = lafter.pop()
                    liveset_old = previous.copy()
                    # Body Sequence
                    lafterbody, instrsbody = livenessSeq(n.body, previous)
                    instrsbody.reverse()
                    lafterbody.reverse()
                    # Test Sequence
                    #sys.stderr.write("n.test          = %s\n" % (str(n.test)))
                    laftertest, instrstest = livenessSeq(n.test, previous)
                    instrstest.reverse()
                    laftertest.reverse()
                    #sys.stderr.write("laftertest      = %s\n" % (str(laftertest[-1])))
                    # Calculate union of test, body, and initial set
                    liveset = lafterbody.pop() | laftertest.pop() | liveset_old
                    if(debug):
                        sys.stderr.write("liveset_old  = %s\n" % (str(liveset_old)))
                        sys.stderr.write("liveset      = %s\n" % (str(liveset)))
                    if(liveset_old == liveset):
                        # Make Permanent Changes
                        instrs += instrsbody
                        lafter += lafterbody
                        instrs += instrstest
                        lafter += laftertest
                        lafter += [liveset]
                        break
                    else:
                        # Propgate intermediate liveset to next loop iteration
                        lafter += [liveset]
                    loopcnt += 1
                    if(loopcnt > MAXLOOPCNT):
                        raise Exception("Loop Liveness Analysis does not seem to be converging...")
            else:
                # Normal Instruction
                instrs += [n]
                instrvars = extractVars(n)
                lafter += [(lafter[-1] - instrvars.written) | instrvars.read]
                
        # Reverse and return lafter
        instrs.reverse()
        lafter.reverse()
        return (lafter[:], instrs)

    lafterfull, instrsfull = livenessSeq(instrs)    
    return (lafterfull[1:], instrsfull);

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
        elif(isinstance(instr, IndirectCall86)):
            if(validNode(instr.function)):
                graph[name(instr.function)] = set([])

        # target only nodes
        elif(isinstance(instr, Neg86) or
             isinstance(instr, SetEq86) or
             isinstance(instr, SetNEq86)):
            if(validNode(instr.target)):
                graph[name(instr.target)] = set([])

        # left right nodes
        # TODO: Combine with target/value
        elif(isinstance(instr, Comp86)):
            if(validNode(instr.value)):
                graph[name(instr.value)] = set([])
            if(validNode(instr.target)):
                graph[name(instr.target)] = set([])

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
        elif(isinstance(instr, Call86) or 
             isinstance(instr, IndirectCall86)):
            for v in live:
                # Add edge for each caller save register
                for reg in CALLERSAVE:
                    if(validNode(reg)):
                        r = name(reg)
                        if(v != r):
                            addEdge(r, v)


        # If small reg
        elif(isinstance(instr, SetEq86) or
             isinstance(instr, SetNEq86)):
            if(validNode(instr.target)):
                t = name(instr.target)
                # Add edge for each string (none GP) register
                for reg in STRINGREGS:
                    if(validNode(reg)):
                        r = name(reg)
                        if(t != r):
                            addEdge(r, t)
                # Loop through live set
                for v in live:
                    # Add edge unless v=t
                    if(v != t):
                        addEdge(t, v)

        # No Action for read only and non-register instructions
        elif(isinstance(instr, Jump86),
             isinstance(instr, JumpEqual86),
             isinstance(instr, Label86),
             isinstance(instr, Push86),
             isinstance(instr, Comp86)):
            pass

        # Unhandled Error
        else:
            #TODO Why Arn't These Being Raised for New Instructions?
            raise Exception("regalloc: Un-handled Node %s" % str(instr))

    # Check Length
    if(len(instrs) != len(lafter)):
        raise Exception("Mismatched lengths")

    # Seed Graph

    for reg in CALLERSAVE:
        if(validNode(reg)):
            graph[name(reg)] = set([])
    for reg in STRINGREGS:
        if(validNode(reg)):
            graph[name(reg)] = set([])
    for instr in instrs:
        addKey(instr)

    # Add edges
    for n in range(len(instrs)):
        updateGraph(instrs[n], lafter[n])

    return graph

def color(graph, colors, regOnlyVars):
    
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
        #priorityKeys = []
        #for key in w:
        #    if(key in regOnlyVars):
        #        priorityKeys += [key]
        # Else use all keys
#        if(len(priorityKeys) == 0):
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
        for key in maxkeys:
            maxkey = key
            if key in regOnlyVars:
                break
        
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
        elif(isinstance(instr, Comp86)):
            return [Move86(instr.value, tmp),
                    Comp86(tmp, instr.target)]
        else:
            raise Exception("Cannot add temp to node: " + str(instr))
    
    fixedInstrs = []
    regOnlyVars = []

    #Loop through instructions
    for instr in instrs:
        
        # Binary read/write
        if(isinstance(instr, Add86) or
           isinstance(instr, Sub86) or
           isinstance(instr, Move86) or
           isinstance(instr, Comp86)):
            if(validNode(instr.target) and 
               validNode(instr.value)):
                # Find mem to mem operations
                if((colors[name(instr.target)] >= len(REGCOLORS)) and
                   (colors[name(instr.value)] >= len(REGCOLORS))):
                    # Add temp var
                    tmp = Var86(generate_name(regTempPrefix))
                    fixedInstrs += addTemp(instr, tmp)
                    regOnlyVars += [tmp.name]
                else:
                    fixedInstrs += [instr]
            elif validNode(instr.target) and isinstance(instr.value, Mem86):
                if(colors[name(instr.target)] >= len(REGCOLORS)):
                    tmp = Var86(generate_name(regTempPrefix))
                    fixedInstrs += addTemp(instr, tmp)
                    regOnlyVars += [tmp.name]
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
            offset = ((color - len(REGCOLORS) + 1) * WORDLEN)
            return Mem86(-offset, EBP)

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
        elif(isinstance(instr, IndirectCall86)):
            if(validNode(instr.function)):
                instr.function = replace(instr.function, colormap)
        
        # Unary write
        # TODO: Combine with unary read/write case above
        elif(isinstance(instr, SetEq86) or
             isinstance(instr, SetNEq86)):
            if(validNode(instr.target)):
                instr.target = replace(instr.target, colormap)

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
            if(validNode(instr.value)):
                instr.value = replace(instr.value, colormap)
            if(validNode(instr.target)):
                instr.target = replace(instr.target, colormap)

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

def fixSmallRegs(instrs):

    def validNode(val):
        return isinstance(val, Reg86)

    def replaceReg(reg):
        return ONEBYTELOWREGS[reg]

    #Duplicate
    instrs = instrs[:]

    #Loop through instructions
    for instr in instrs:

        # Single Byte Instructions
        if(isinstance(instr, SetEq86) or
           isinstance(instr, SetNEq86)):
            if(validNode(instr.target)):
                instr.target = replaceReg(instr.target)

        # No Change Necessary
        else:
            pass

    return instrs

def maxColor(colors):
    maxcolor = -1
    for key in colors:
        color = colors[key]
        if(color > maxcolor):
            maxcolor = color
    return maxcolor

def addPreamble(instrs, colors):
    stackvars = max((maxColor(colors) - len(REGCOLORS) + 1), 0)
    offset = 2 + len(CALLEESAVE) # retAddr push + EBP push + CalleeSave pushes
    preamble = [Push86(EBP),
                Move86(ESP, EBP)]
    stackvars += (STACKALIGN - ((stackvars + offset) % STACKALIGN))
    preamble += [Sub86(Const86(stackvars * WORDLEN), ESP)]
    saveregs = CALLEESAVE[:]
    for reg in saveregs:
        preamble += [Push86(reg)]
    return preamble + instrs

def addClosing(instrs, funcName):
    closing  = [Label86(generate_return_label(funcName))]
    saveregs = CALLEESAVE[:]
    saveregs.reverse()
    for reg in saveregs:
        closing += [Pop86(reg)]
    closing += [Leave86()]
    closing += [Ret86()]
    return instrs + closing

def regAlloc(instrs, regOnlyVars, funcName):

    (lafter, instrseq) = liveness(instrs)
    if(debug):
        sys.stderr.write("lafter      =\n" + "\n".join(map(str, lafter)) + "\n")
    graph = interference(instrseq, lafter)
    if(debug):
        sys.stderr.write("graph       =\n" + str(graph) + "\n")
    colors = color(graph, {}, regOnlyVars)
    if(debug):
        sys.stderr.write("colors      =\n" + str(colors) + "\n")
    iterations = 0
    while(1):

        (instrseq, newRegOnlyVars) = fixMemToMem(instrseq, colors)
        fixcnt = len(newRegOnlyVars)
        regOnlyVars += newRegOnlyVars

        if(debug):
            sys.stderr.write("regOnlyVars =\n" + str(regOnlyVars) + "\n")
            sys.stderr.write("fixcnt =\n" + str(fixcnt) + "\n")
            sys.stderr.write("iterations =\n" + str(iterations) + "\n")

        if(fixcnt == 0):
            break

        lafter, instrseq = liveness(instrseq)
        graph = interference(instrseq, lafter)
        colors = color(graph, colors, regOnlyVars)
        iterations += 1

        if(iterations > MAXITERATIONS):
            raise Exception("Could not complete register allocation withen iteration limit")
        
    instrseq = varReplace(instrseq, colors)
    instrseq = fixSmallRegs(instrseq)
    instrseq = addPreamble(instrseq, colors)
    instrseq = addClosing(instrseq, funcName)

    return instrseq

def funcRegAlloc(funcs):
    outFuncs = []
    for func in funcs:
        outFuncs += [Func86(func.name, regAlloc(func.nodes, [], func.name))]
    return outFuncs
