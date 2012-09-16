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
TEST USAGE:
    lexer5525.py <file path>
"""

import sys

import ply.lex as lex

# Tokens

tokens = ('PRINT', 'INPUT',
          'INT',
          'PLUS', 'UMINUS',
          'NAME', 'ASSIGN',
          'LPAREN', 'RPAREN')


t_PRINT  = r'print'
t_INPUT  = r'input'

def t_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        sys.stderr.write("integer value too large\n", t.value)
        t.value = 0
    return t

t_PLUS   = r'\+'
t_UMINUS = r'\-'
t_NAME   = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ASSIGN = r'='
t_LPAREN  = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    sys.stderr.write("Illegal charecter '%s'\n" % t.value[0])
    t.lexer.skip(1)

lex.lex()

### Test Function ###

def main(argv=None):
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

    data = '''x=4
-input() + 5
print x
'''

    lex.input(data)

    while True:
        tok = lex.token()
        if not tok:
            break
        sys.stdout.write(str(tok) + "\n")

    return 0
    
if __name__ == "__main__":
    sys.exit(main())
