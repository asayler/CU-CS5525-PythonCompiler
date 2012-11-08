# CU CS5525
# Fall 2012
# Python Compiler
#
# graph_preprocessedast.py
# Visitor to graph a monoAST
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

from graph_ast import Graph_ast

class Graph_preprocessedast(Graph_ast):

    def visitSubscriptAssign(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("SubscriptAssign(%s)" % str(n.sub)))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.target, myid)
        lines += self.dispatch(n.value, myid)
        return lines

    def visitAttrAssign(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("AttrAssign(%s)" % str(n.attr)))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.target, myid)
        lines += self.dispatch(n.value, myid)
        return lines
