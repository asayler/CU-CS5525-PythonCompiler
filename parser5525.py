#!/usr/bin/python

# Andy Sayler
# Fall 2012
# CU CS5525
# Python Parser
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

"""
PARSER TEST USAGE:
    parser5525.py <file path>
"""

import sys

import ply.yacc as yacc

from compiler.ast import *
from lexer5525 import tokens

def parser5525_TestMain(argv=None):
    """Parser Test Cases"""

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

    inputFile = open(inputFilePath)
    source = inputFile.read()
    inputFile.close()

    #lex.input(source)

    #while True:
    #    tok = lex.token()
    #    if not tok:
    #        break
    
    sys.stdout.write(str(tokens) + "\n")

    return 0
    
if __name__ == "__main__":
    sys.exit(parser5525_TestMain())
