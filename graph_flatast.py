# Andy Sayler
# Fall 2012
# CU CS5525
# Python Compiler
# Visitor to graph a flatAST
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
from flatast import *

from graphvis_dot import Graphvis_dot

from graph_expandedast import Graph_expandedast

class Graph_flatast(Graph_expandedast):
    
    # Banned Nodes

    def visitmono_Let(self, n, p):
        raise Exception("'mono_:et' node no longer valid at this stage")

    # New Nodes

    def visitflat_InstrSeq(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("flat_InstrSeq"))
        lines += Graphvis_dot().linePair(p, myid)
        for node in n.nodes:
            lines += self.dispatch(node, myid)
        lines += self.dispatch(n.expr, myid)
        return lines
