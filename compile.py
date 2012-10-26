#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# compile.py
# Top Level "Main" Compile Script
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

"""
USAGE:
    compile.py <file path>
"""

import sys, compiler

# Data Types
from compiler.ast import *
from monoast import *
from x86ast import *

# Compiler Stages
from explicate import *
from heapify import *
from closureconvert import *
from expand import *
from flatten import *
from instr_select import *
from x86regalloc import *

# Helper Tools
from astTools import *
from graph_ast import *
from graph_monoast import *
from graph_closedast import *
from graph_expandedast import *
from graph_flatast import *

debug = True

def write_to_file(assembly, outputFileName):
    """Function to write assembly to file"""
    assembly = '\n'.join(map(lambda x: x.mnemonic(), assembly))
    outputfile = open(outputFileName, 'w+')
    outputfile.write(assembly + '\n')
    outputfile.close()

### Main Function ###

def main(argv=None):
    """Main Compiler Entry Point Function"""

    # Setup and Check Args
    if argv is None:
        argv = sys.argv

    if len(argv) != 2:
        sys.stderr.write(str(argv[0]) + " requires two arguments\n")
        sys.stderr.write(__doc__ + "\n")
        return 1

    inputFilePath = str(argv[1])

    if(inputFilePath[-3:] != ".py"):
        sys.stderr.write(str(argv[0]) + " input file must be of type *.py\n")
        return 1

    outputFilePath = inputFilePath.split('/')
    outputFileName = (outputFilePath[-1:])[0]
    outputFileName = outputFileName[:-3] + ".s"

    if(debug):
        sys.stderr.write(str(argv[0]) + ": inputFilePath = " + inputFilePath + "\n")
        sys.stderr.write(str(argv[0]) + ": outputFilePath = " + str(outputFileName) + "\n")
    
    # Parse inputFile
    parsedast = compiler.parseFile(inputFilePath)
    if(debug):
        # Print parsedast
        sys.stderr.write("parsed ast = \n" + str(parsedast) + "\n")
        # Graph parsedast
        debugFileName = (outputFilePath[-1:])[0]
        debugFileName = debugFileName[:-3] + "-parsed.dot"
        Graph_ast().writeGraph(parsedast, debugFileName)

    # Explicate
    monoast = ExplicateVisitor().preorder(parsedast)
    if(debug):
        # Print monoast
        #sys.stderr.write("mono ast = \n" + str(monoast) + "\n")
        # Graph monoast
        debugFileName = (outputFilePath[-1:])[0]
        debugFileName = debugFileName[:-3] + "-explicated.dot"
        Graph_monoast().writeGraph(monoast, debugFileName)        

    # Heapify
    heapast = HeapifyVisitor().preorder(monoast)
    if(debug):
        # Print heapast
        sys.stderr.write("heapified ast = \n" + str(heapast) + "\n")
        # Graph monoast
        debugFileName = (outputFilePath[-1:])[0]
        debugFileName = debugFileName[:-3] + "-heapified.dot"
        Graph_monoast().writeGraph(heapast, debugFileName)

    # Closure COnvert
    closedast = ClosureVisitor().preorder(heapast)
    if(debug):
        # Print heapast
        sys.stderr.write("closed ast = \n" + str(closedast) + "\n")
        # Graph monoast
        debugFileName = (outputFilePath[-1:])[0]
        debugFileName = debugFileName[:-3] + "-closed.dot"
        Graph_closedast().writeGraph(closedast, debugFileName)

    # Exit Early Since Further Stages Not Yet Implmented for p2
    # Type Check
    # TODO

    # Expand
    expandedast = ExpandVisitor().preorder(closedast)
    if(debug):
        # Print expandedast
        #sys.stderr.write("expanded ast = \n" + str(expandedast) + "\n")
        # Graph expandedast
        debugFileName = (outputFilePath[-1:])[0]
        debugFileName = debugFileName[:-3] + "-expanded.dot"
        Graph_expandedast().writeGraph(expandedast, debugFileName)
    
    # Flatten Tree
    flatast = FlattenVisitor().preorder(expandedast)
    if(debug):
        # Print flatast
        #sys.stderr.write("flat ast = \n" + str(flatast) + "\n")
        # Graph flatast
        debugFileName = (outputFilePath[-1:])[0]
        debugFileName = debugFileName[:-3] + "-flat.dot"
        Graph_flatast().writeGraph(flatast, debugFileName)
        
    # Compile flat tree
    assembly = InstrSelectVisitor().preorder(flatast)
    if(debug):
        pass
        #sys.stderr.write("instr ast = \n" + "\n".join(map(str, assembly)) + "\n")

    #Exit Early
    return 1

    # Reg Alloc
    assembly = regAlloc(assembly)
    if(debug):
        pass
        #sys.stderr.write("instrs = \n" + "\n".join(map(str, assembly)) + "\n")

    # Write output
    write_to_file(map(str, assembly), outputFileName)

    return 0

if __name__ == "__main__":
    sys.exit(main())
