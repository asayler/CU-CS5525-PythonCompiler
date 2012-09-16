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

# Parsing Rules

precedence = (('nonassoc', 'PRINT'),
              ('nonassoc', 'INPUT'),
              ('left', 'ADD'),
              ('right', 'UMINUS'),
              ('nonassoc', 'LPAREN'))
              
def p_module(p):
    'module : stmt_list'
    p[0] = Module(None, Stmt(p[1]))

def p_stmt_list_multi(p):
    'stmt_list : stmt stmt_list'
    p[0] = [p[1]] + p[2]

def p_stmt_list_single(p):
    'stmt_list : stmt'
    p[0] = [p[1]]

def p_stmt_list_none(p):
    'stmt_list : empty'
    p[0] = []

def p_stmt_print(p):
    'stmt : PRINT expr' 
    p[0] = Printnl([p[2]], None)

def p_stmt_assign(p):
    'stmt : assignee ASSIGN expr' 
    p[0] = Assign([p[1]], p[3])

def p_stmt_expr(p):
    'stmt : expr' 
    p[0] = Discard(p[1])

def p_assignee(p):
    'assignee : NAME'
    p[0] = AssName(p(1), 'OP_ASSIGN')

def p_empty(p):
    'empty :'
    pass

# Test Main

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
