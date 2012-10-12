# Andy Sayler
# Fall 2012
# CU CS5525
# Python Compiler
# Visitor to graph a monoAST
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

from graph_ast import Graph_ast

class Graph_monoast(Graph_ast):
    
    # Banned Nodes

    def visitAdd(self, n, p):
        raise Exception("AST 'Add' node no longer valid at this stage")

    # New Nodes

    def visitmono_IntAdd(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("mono_Add"))
        lines += Graphvis_dot().linePair(p, n)
        lines += self.dispatch(n.left, n)
        lines += self.dispatch(n.right, n)
        return lines

    def visitmono_ProjectTo(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("mono_ProjectTo(%s)" % str(n.typ.typ)))
        lines += Graphvis_dot().linePair(p, n)
        lines += self.dispatch(n.arg, n)
        return lines

    def visitmono_InjectFrom(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("mono_InjectFrom(%s)" % str(n.typ.typ)))
        lines += Graphvis_dot().linePair(p, n)
        lines += self.dispatch(n.arg, n)
        return lines

    def visitmono_IsTag(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("mono_IsTag(%s)" % str(n.typ.typ)))
        lines += Graphvis_dot().linePair(p, n)
        lines += self.dispatch(n.arg, n)
        return lines

    def visitmono_Let(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("mono_Let"))
        lines += Graphvis_dot().linePair(p, n)
        lines += self.dispatch(n.var, n)
        lines += self.dispatch(n.rhs, n)
        lines += self.dispatch(n.body, n)
        return lines

    def visitmono_IsTrue(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("mono_IsTrue"))
        lines += Graphvis_dot().linePair(p, n)
        lines += self.dispatch(n.expr, n)
        return lines
