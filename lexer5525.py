#!/usr/bin/python

# Andy Sayler
# Fall 2012
# CU CS5525
# Python Lexer
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

"""
LEXER TEST USAGE:
    lexer5525.py <file path>
"""

import sys

import ply.lex as lex

# Tokens

reserved = {'print' : 'PRINT'}

tokens = ['NAME', 'INT',
          'PLUS', 'MINUS', 'ASSIGN',
          'LPAREN', 'RPAREN'] + list(reserved.values())

def t_NAME(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value, 'NAME')
    return t

def t_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        sys.stderr.write("integer value too large\n", t.value)
        t.value = 0
    return t

t_PLUS   = r'\+'
t_MINUS = r'\-'
t_ASSIGN = r'='
t_LPAREN  = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

# Other

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Errors

def t_error(t):
    sys.stderr.write("Illegal charecter '%s'\n" % t.value[0])
    t.lexer.skip(1)

# Build Lexer

lex.lex()

### Test Function ###

def lexer5525_TestMain(argv=None):
    """Lexer Test Cases"""

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

    lex.input(source)

    while True:
        tok = lex.token()
        if not tok:
            break
        sys.stdout.write(str(tok) + "\n")

    return 0
    
if __name__ == "__main__":
    sys.exit(lexer5525_TestMain())
