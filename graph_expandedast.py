# CU CS5525
# Fall 2012
# Python Compiler
#
# graph_expandedast.py
# Visitor to graph an expanded AST
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

    def visitIsTag(self, n, p):
        raise Exception("'IsTag' node no longer valid at this stage")

    def visitProjectTo(self, n, p):
        raise Exception("'ProjectTo' node no longer valid at this stage")

    def visitInjectFrom(self, n, p):
        raise Exception("'InjectFrom' node no longer valid at this stage")

    def visitAnd(self, n, p):
        raise Exception("'And' node no longer valid at this stage")

    def visitOr(self, n, p):
        raise Exception("'Or' node no longer valid at this stage")

    def visitIfExp(self, n, p):
        raise Exception("'IfExp' node no longer valid at this stage")

    def visitSubscript(self, n, p):
        raise Exception("'Subscript' node no longer valid at this stage")

    def visitSubscriptAssign(self, n, p):
        raise Exception("'SubscriptAssign' node no longer valid at this stage")

    # New Nodes
    def visitIfExp(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("IfExp"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.test, myid)
        lines += self.dispatch(n.then, myid)
        lines += self.dispatch(n.else_, myid)
        return lines
