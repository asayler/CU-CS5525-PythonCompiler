# CU CS5525
# Fall 2012
# Python Compiler
#
# flatast.py
# Flat AST Node
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

from compiler.ast import *

class flat_Node:
    """Abstract base class for flatast nodes"""
    # Do nothing, just a placeholder in case we want to add to it later

# New Mono Nodes

class flat_InstrSeq(flat_Node):
    def __init__(self, nodes, expr):
        self.nodes = nodes
        self.expr = expr
    def __repr__(self):
        return "flat_InstrSeq(%s, %s)" % (repr(self.nodes), repr(self.expr))
