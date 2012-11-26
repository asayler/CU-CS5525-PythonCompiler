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

import sys

# Compiler Stages
from declassify import *
from uniquify import *
from explicate import *
from heapify import *
from closureconvert import *
from expand import *
from flatten import *
from instr_select import *
from x86regalloc import *
from stringfind import *

# Helper Tools
from graph_visitor import *

parser = 'CURRENT'

if parser == 'DEPRECATED':
    from depr_parse import *
elif parser == 'CURRENT':
    from py3parse import *
else:
    raise Exception('Invalid parser name')

debug = False

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
    outputFileBase = (outputFilePath[-1:])[0]
    outputFileName = outputFileBase[:-3] + ".s"

    if(debug):
        sys.stderr.write(str(argv[0]) + ": inputFilePath = " + inputFilePath + "\n")
        sys.stderr.write(str(argv[0]) + ": outputFilePath = " + str(outputFileName) + "\n")
    
    # Parse inputFile
    parsedast = parse(inputFilePath)
    if(debug):
        # Print parsedast
        sys.stderr.write("parsed ast = \n" + str(parsedast) + "\n")
        # Graph parsedast
        debugFileName = outputFileBase[:-3] + "-parsed.dot"
        GraphVisitor().writeGraph(parsedast, debugFileName)
    
    # Declassify
    declassifiedast = ClassFindVisitor().preorder(parsedast, set([]))
    parsedast = None
    if(debug):
        # Print parsedast
        sys.stderr.write("declassified ast = \n" + str(declassifiedast) + "\n")
        # Graph parsedast
        debugFileName = outputFileBase[:-3] + "-declassified.dot"
        GraphVisitor().writeGraph(declassifiedast, debugFileName)    

    # Uniquify
    uniqueast = UniquifyVisitor().preorder(declassifiedast)
    declassifiedast = None
    if(debug):
        # Print uniqueast
        sys.stderr.write("unique ast = \n" + str(uniqueast) + "\n")
        # Graph uniqueast
        debugFileName = outputFileBase[:-3] + "-uniquified.dot"
        GraphVisitor().writeGraph(uniqueast, debugFileName)

    # Explicate
    monoast = ExplicateVisitor().preorder(uniqueast)
    uniqueast = None
    if(debug):
        # Print monoast
        sys.stderr.write("mono ast = \n" + str(monoast) + "\n")
        # Graph monoast
        debugFileName = outputFileBase[:-3] + "-explicated.dot"
        GraphVisitor().writeGraph(monoast, debugFileName)        

    # Heapify
    heapast = HeapifyVisitor().preorder(monoast)
    monoast = None
    if(debug):
        # Print heapast
        sys.stderr.write("heapified ast = \n" + str(heapast) + "\n")
        # Graph monoast
        debugFileName = outputFileBase[:-3] + "-heapified.dot"
        GraphVisitor().writeGraph(heapast, debugFileName)

    # Closure COnvert
    closedast = ClosureVisitor().preorder(heapast)
    heapast = None
    if(debug):
        # Print heapast
        sys.stderr.write("closed ast = \n" + str(closedast) + "\n")
        # Graph monoast
        debugFileName = outputFileBase[:-3] + "-closed.dot"
        GraphVisitor().writeGraph(closedast, debugFileName)
   
    # Type Check
    # TODO

    # Expand
    expandedast = ExpandVisitor().preorder(closedast)
    closedast = None
    if(debug):
        # Print expandedast
        sys.stderr.write("expanded ast = \n" + str(expandedast) + "\n")
        # Graph expandedast
        debugFileName = outputFileBase[:-3] + "-expanded.dot"
        GraphVisitor().writeGraph(expandedast, debugFileName)
    
    # Flatten Tree
    flatast = FlattenVisitor().preorder(expandedast, True)
    expandedast = None
    if(debug):
        # Print flatast
        sys.stderr.write("flat ast = \n" + str(flatast) + "\n")
        # Graph flatast
        debugFileName = outputFileBase[:-3] + "-flat.dot"
        GraphVisitor().writeGraph(flatast, debugFileName)

    # Compile flat tree
    (strings, assembly) = InstrSelectVisitor().preorder(flatast)
    flatast = None
    if(debug):
        sys.stderr.write("pre  instr ast = \n" + str(assembly) + "\n")

    # Reg Alloc
    assembly = setup_strings(strings) + funcRegAlloc(assembly)
    if(debug):
        sys.stderr.write("post instr ast = \n" + str(assembly) + "\n")
    
    # Write output
    write_to_file(assembly, outputFileName)

    return 0

if __name__ == "__main__":
    sys.exit(main())
