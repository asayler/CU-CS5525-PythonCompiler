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

    def visitLambda(self, n, p):
        raise Exception("'Lambda' node no longer valid at this stage")

    def visitFunction(self, n, p):
        raise Exception("'Function' node no longer valid at this stage")

    # New Nodes

    def visitIntAdd(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("IntAdd"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.left, myid)
        lines += self.dispatch(n.right, myid)
        return lines

    def visitIntUnarySub(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("IntUnarySub"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.expr, myid)
        return lines

    def visitIntEqual(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("IntEqual"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.left, myid)
        lines += self.dispatch(n.right, myid)
        return lines 

    def visitIntNotEqual(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("IntNotEqual"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.left, myid)
        lines += self.dispatch(n.right, myid)
        return lines 

    def visitProjectTo(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("ProjectTo(%s)" % str(n.typ.typ)))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.arg, myid)
        return lines

    def visitInjectFrom(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("InjectFrom(%s)" % str(n.typ.typ)))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.arg, myid)
        return lines

    def visitIsTag(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("IsTag(%s)" % str(n.typ.typ)))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.arg, myid)
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

    def visitSubscriptAssign(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("SubscriptAssign"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.target, myid)
        lines += self.dispatch(n.sub, myid)
        lines += self.dispatch(n.value, myid)
        return lines

    def visitSLambda(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("SLambda(%s)" % n.params))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.body, myid)
        return lines

    def visitIndirectCallFunc(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("IndirectCallFunc"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.name, myid)
        for arg in n.args:
            lines += self.dispatch(arg, myid)
        return lines

