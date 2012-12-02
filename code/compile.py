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

# External Imports
import sys
import argparse

# Compiler Stage Imports

from declassify import ClassFindVisitor
from uniquify import UniquifyVisitor
from explicate import ExplicateVisitor
from heapify import HeapifyVisitor
from closureconvert import ClosureVisitor
from expand import ExpandVisitor
from flatten import FlattenVisitor
from ssa import SSAVisitor

from x86regalloc import x86funcRegAlloc
from x86regalloc import x86setup_strings
from x86instr_select import x86InstrSelectVisitor

from llvminstr_select import LLVMInstrSelectVisitor


# Helper Tool Imports
from graph_visitor import GraphVisitor

DECLARESFILE = './helper/runtime-declares.ll'
PARSER = 'CURRENT'

if PARSER == 'DEPRECATED':
    from depr_parse import *
elif PARSER == 'CURRENT':
    from py3parse import *
else:
    raise Exception('Invalid parser name')

def write_to_file(assembly, outputFilePath):
    """Function to write assembly to file"""
    assembly = '\n'.join(map(lambda x: str(x), assembly))
    outputfile = open(outputFilePath, 'w')
    outputfile.write(assembly + '\n')
    outputfile.close()

def read_declares_file(declaresFilePath):
    """Function to read LLVM 'declare' statments from a file"""
    declares = []
    inputFile = open(declaresFilePath, 'r')
    for line in inputFile:
        cline = line.replace('\n', '')
        words = cline.split()
        if(len(words) > 0):
            if(words[0] == 'declare'):
                declares += [cline]
    return declares

### Main Function ###

def main(argv=None):
    """Main Compiler Entry Point Function"""

    if argv is None:
        argv = sys.argv

    # Setup and Check Args

    parser = argparse.ArgumentParser(description='Compile a Python file')
    parser.add_argument('inputfilepath',
                        help='Input File Path')
    parser.add_argument('-o', dest='outputfilepath', default=None,
                        help='Output File Path')
    parser.add_argument('--dot', dest='dotfileflag', action='store_const', const=True,
                        help='Generate Dot Files')
    parser.add_argument('--dotdir', dest='dotfiledirectory', default=None,
                        help='Dot File Output Directory')
    parser.add_argument('-v', dest='verbosity', type=int, default=0,
                        help='Compiler Verbosity')
    args = parser.parse_args(argv[1:])

    inputFilePath     = args.inputfilepath
    inputFilePathList = inputFilePath.split('/')
    inputFileName     = (inputFilePathList[-1:])[0]
    inputFileNameList = inputFileName.split('.')
    inputFileNameExt  = (inputFileNameList[-1:])[0]
    if(inputFileNameExt != "py"):
        sys.stderr.write(str(argv[0]) + ": input file must be of type *.py\n")
        return 1

    outputFilePath     = args.outputfilepath
    if(outputFilePath == None):
        outputFilePath = inputFileName[:-3] + ".s"
    outputFilePathList = outputFilePath.split('/')
    outputFileName     = (outputFilePathList[-1:])[0]
    outputFileNameList = outputFileName.split('.')
    outputFileNameBase = '.'.join(outputFileNameList[:-1])
    outputFileNameExt  = (outputFileNameList[-1:])[0]
    if(outputFileNameExt == "s"):
        compileType = "x86"
    elif(outputFileNameExt == "ll"):
        compileType = "LLVM"
    else:
        sys.stderr.write(str(argv[0]) + ": unrecognized output file type\n")
        return 1

    dotFileDir      = args.dotfiledirectory
    if(dotFileDir == None):
        dotFileDir  = '/'.join(outputFilePathList[:-1])
    dotFileDirList  = dotFileDir.split('/')
    dotFileNameBase = outputFileNameBase
    dotFileNameExt  = ".dot"
    dotFilePath     = dotFileDir + dotFileNameBase

    dotFileFlag = args.dotfileflag
    debug       = args.verbosity

    if(debug):
        sys.stderr.write(str(argv[0]) + ": inputFilePath  = " + inputFilePath + "\n")
        sys.stderr.write(str(argv[0]) + ": outputFilePath = " + outputFilePath + "\n")
    
    # Parse inputFile
    parsedast = parse(inputFilePath)
    if(debug):
        # Print ast
        sys.stderr.write("parsed ast = \n" + str(parsedast) + "\n")
    if(dotFileFlag):
        # Graph ast
        dotFileName = dotFilePath + "-parsed" + dotFileNameExt
        GraphVisitor().writeGraph(parsedast, dotFileName)
    
    # Declassify
    declassifiedast = ClassFindVisitor().preorder(parsedast, set([]))
    parsedast = None
    if(debug):
        # Print ast
        sys.stderr.write("declassified ast = \n" + str(declassifiedast) + "\n")
    if(dotFileFlag):
        # Graph ast
        dotFileName = dotFilePath + "-declassified" + dotFileNameExt
        GraphVisitor().writeGraph(declassifiedast, dotFileName)

    # Uniquify
    uniqueast = UniquifyVisitor().preorder(declassifiedast)
    declassifiedast = None
    if(debug):
        # Print ast
        sys.stderr.write("unique ast = \n" + str(uniqueast) + "\n")
    if(dotFileFlag):
        # Graph ast
        dotFileName = dotFilePath + "-uniquified" + dotFileNameExt
        GraphVisitor().writeGraph(uniqueast, dotFileName)

    # Explicate
    monoast = ExplicateVisitor().preorder(uniqueast)
    uniqueast = None
    if(debug):
        # Print ast
        sys.stderr.write("mono ast = \n" + str(monoast) + "\n")
    if(dotFileFlag):
        # Graph ast
        dotFileName = dotFilePath + "-explicated" + dotFileNameExt
        GraphVisitor().writeGraph(monoast, dotFileName)        

    # Heapify
    heapast = HeapifyVisitor().preorder(monoast)
    monoast = None
    if(debug):
        # Print ast
        sys.stderr.write("heapified ast = \n" + str(heapast) + "\n")
    if(dotFileFlag):
        # Graph ast
        dotFileName = dotFilePath + "-heapified" + dotFileNameExt
        GraphVisitor().writeGraph(heapast, dotFileName)

    # Closure COnvert
    closedast = ClosureVisitor().preorder(heapast)
    heapast = None
    if(debug):
        # Print ast
        sys.stderr.write("closed ast = \n" + str(closedast) + "\n")
    if(dotFileFlag):
        # Graph ast
        dotFileName = dotFilePath + "-closed" + dotFileNameExt
        GraphVisitor().writeGraph(closedast, dotFileName)
   
    # Type Check
    # TODO

    # Expand
    expandedast = ExpandVisitor().preorder(closedast)
    closedast = None
    if(debug):
        # Print ast
        sys.stderr.write("expanded ast = \n" + str(expandedast) + "\n")
    if(dotFileFlag):
        # Graph ast
        dotFileName = dotFilePath + "-expanded" + dotFileNameExt
        GraphVisitor().writeGraph(expandedast, dotFileName)
    
    # Flatten Tree
    flatast = FlattenVisitor().preorder(expandedast, True)
    expandedast = None
    if(debug):
        # Print ast
        sys.stderr.write("flat ast = \n" + str(flatast) + "\n")
    if(dotFileFlag):
        # Graph ast
        dotFileName = dotFilePath + "-flat" + dotFileNameExt
        GraphVisitor().writeGraph(flatast, dotFileName)

    if(compileType == "x86"):

        # Compile flat tree
        (strings, assembly) = x86InstrSelectVisitor().preorder(flatast)
        flatast = None
        if(debug):
            sys.stderr.write("pre  instr ast = \n" + str(assembly) + "\n")

        # Reg Alloc
        assembly = x86setup_strings(strings) + x86funcRegAlloc(assembly)
        if(debug):
            sys.stderr.write("post instr ast = \n" + str(assembly) + "\n")

    elif(compileType == "LLVM"):

        # SSA conversion
        ssast = SSAVisitor().preorder(flatast)
        flatast = None
        
        # Compile to LLVM
        llvm = LLVMInstrSelectVisitor().preorder(ssast)
        ssast = None

        # Add external declare statments
        declares = read_declares_file(DECLARESFILE)
        assembly = declares + llvm

    else:

        sys.stderr.write(str(argv[0]) + ": unrecognized compileType\n")
        return 1


    # Write output
    write_to_file(assembly, outputFilePath)

    return 0

if __name__ == "__main__":
    sys.exit(main())
