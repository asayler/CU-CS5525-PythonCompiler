# Andy Sayler
# Fall 2012
# CU CS5525
# Python Compiler
# Flat Intermediate AST Nodes
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

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
