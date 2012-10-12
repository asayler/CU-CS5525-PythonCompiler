# Andy Sayler
# Fall 2012
# CU CS5525
# Python Compiler
# Visitor to graph an expandedAST
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

import sys
import compiler

from compiler.ast import *
from monoast import *

from graphvis_dot import Graphvis_dot

from graph_monoast import Graph_monoast

class Graph_expandedast(Graph_monoast):
    
    # Banned Nodes

    def visitPrintnl(self, n, p):
        raise Exception("AST 'Printnl' node no longer valid at this stage")

    def visitmono_IsTag(self, n, p):
        raise Exception("'mono_IsTag' node no longer valid at this stage")

    def visitmono_ProjectTo(self, n, p):
        raise Exception("'mono_ProjectTo' node no longer valid at this stage")

    def visitmono_InjectFrom(self, n, p):
        raise Exception("'mono_InjectFrom' node no longer valid at this stage")

    def visitAnd(self, n, p):
        raise Exception("'And' node no longer valid at this stage")

    def visitOr(self, n, p):
        raise Exception("'Or' node no longer valid at this stage")
