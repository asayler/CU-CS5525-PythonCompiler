# CU CS5525
# Fall 2012
# Python Compiler
#
# graph_declassifiedast.py
# Visitor to graph a declassffiedAST
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
from pyast import *

from graphvis_dot import Graphvis_dot

from graph_preprocessedast import Graph_preprocessedast

class Graph_declassifiedast(Graph_preprocessedast):

    def visitString(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("'%s'" % n.string))
        lines += Graphvis_dot().linePair(p, myid)
        return lines

    def visitLet(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("Let"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.var, myid)
        lines += self.dispatch(n.rhs, myid)
        lines += self.dispatch(n.body, myid)
        return lines

