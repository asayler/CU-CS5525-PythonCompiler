# CU CS5525
# Fall 2012
# Python Compiler
#
# graph_monoast.py
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

class Graph_monoast(Graph_ast):
    
    # Banned Nodes

    def visitAdd(self, n, p):
        raise Exception("'Add' node no longer valid at this stage")

    def visitNot(self, n, p):
        raise Exception("'Not' node no longer valid at this stage")

    def visitUnarySub(self, n, p):
        raise Exception("'UnarySub' node no longer valid at this stage")

    def visitCompare(self, n, p):
        raise Exception("'Compare' node no longer valid at this stage")

    # New Nodes

    def visitmono_IntAdd(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("mono_IntAdd"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.left, myid)
        lines += self.dispatch(n.right, myid)
        return lines

    def visitmono_IntUnarySub(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("mono_IntUnarySub"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.expr, myid)
        return lines

    def visitmono_IntEqual(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("mono_IntEqual"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.left, myid)
        lines += self.dispatch(n.right, myid)
        return lines 

    def visitmono_IntNotEqual(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("mono_IntNotEqual"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.left, myid)
        lines += self.dispatch(n.right, myid)
        return lines 

    def visitmono_ProjectTo(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("mono_ProjectTo(%s)" % str(n.typ.typ)))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.arg, myid)
        return lines

    def visitmono_InjectFrom(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("mono_InjectFrom(%s)" % str(n.typ.typ)))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.arg, myid)
        return lines

    def visitmono_IsTag(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("mono_IsTag(%s)" % str(n.typ.typ)))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.arg, myid)
        return lines

    def visitmono_Let(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("mono_Let"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.var, myid)
        lines += self.dispatch(n.rhs, myid)
        lines += self.dispatch(n.body, myid)
        return lines

    def visitmono_SubscriptAssign(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("mono_SubscriptAssing"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.target, myid)
        lines += self.dispatch(n.sub, myid)
        lines += self.dispatch(n.value, myid)
        return lines
