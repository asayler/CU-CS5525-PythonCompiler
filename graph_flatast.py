# CU CS5525
# Fall 2012
# Python Compiler
#
# graph_flatast.py
# Visitor to graph a flat AST
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

from graph_expandedast import Graph_expandedast

class Graph_flatast(Graph_expandedast):
    
    # Banned Nodes

    def visitLet(self, n, p):
        raise Exception("'Let' node no longer valid at this stage")

    # New Nodes

    def visitInstrSeq(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("InstrSeq"))
        lines += Graphvis_dot().linePair(p, myid)
        for node in n.nodes:
            lines += self.dispatch(node, myid)
        lines += self.dispatch(n.expr, myid)
        return lines

    def visitWhileFlat(self, n, p):
        lines = []
        myid = Graphvis_dot(). uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("WhileFlat"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.testss, myid)
        lines += self.dispatch(n.test, myid)
        lines += self.dispatch(n.body, myid)
        return lines
