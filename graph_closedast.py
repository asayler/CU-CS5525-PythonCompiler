# CU CS5525
# Fall 2012
# Python Compiler
#
# graph_closed.py
# Visitor to graph a closedAST
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

class Graph_closedast(Graph_monoast):
    
    # Banned Nodes


    # Override Nodes
    def visitModule(self, n):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, "Module")
        for node in n.node:
            lines += self.dispatch(node, myid)
        return lines

    # New Nodes

    def visitSLambdaLabel(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("SLambdaLabel(%s)" % n.name))
        lines += Graphvis_dot().linePair(p, myid)
        return lines
