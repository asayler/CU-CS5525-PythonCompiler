#!/usr/bin/python

# Andy Sayler
# CU CS5525
# Python Compiler

"""
USAGE:
    compile.py <file path>
"""

import compiler
import sys

def main(argv=None):

    # Setup and Check Args
    if argv is None:
        argv = sys.argv
    if len(argv) != 2:
        sys.stderr.write(str(argv[0]) + " requires two arguments\n")
        sys.stderr.write(__doc__ + "\n")
        return 1
    inputFilePath = str(argv[1])
    sys.stderr.write(str(argv[0]) + ": inputFilePath = " + inputFilePath + "\n")
    
    # Parse inputFile
    ast = compiler.parseFile(inputFilePath)
    sys.stderr.write(str(argv[0]) + ": ast = " + str(ast) + "\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
