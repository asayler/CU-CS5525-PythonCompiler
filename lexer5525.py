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

import sys

import ply.lex as lex

# Tokens

tokens = ('PRINT', 'INPUT'
          'INT',
          'PLUS', 'UMINUS',
          'NAME', 'ASSIGN'
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
t_PAREN  = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    sys.stderr.write("Illegal charecter '%s'\n" % t.value[0])
    t.lexer.skip(1)

lex.lex()
