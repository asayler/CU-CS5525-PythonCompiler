# CU CS5525
# Fall 2012
# Python Compiler
#
# graph_ast.py
# Visitor to graph a parsed AST
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

import sys, uuid
import compiler

from compiler.ast import *
from monoast import *

from vis import Visitor
from graphvis_dot import Graphvis_dot

class Graph_ast(Visitor):

    def writeGraph(self, ast, filepath):
        lines = self.preorder(ast)
        Graphvis_dot().drawGraph(lines, filepath)

    # Modules

    def visitModule(self, n):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, "Module")
        lines += self.dispatch(n.node, myid)
        return lines
        
    # Statements    

    def visitStmt(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, "Stmt")
        lines += Graphvis_dot().linePair(p, myid)
        for s in n.nodes:
            lines += self.dispatch(s, myid)
        return lines
            
    def visitPrintnl(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, "Printnl")
        lines += Graphvis_dot().linePair(p, myid)
        for node in n.nodes:
            lines += self.dispatch(node, myid)
        return lines

    def visitAssign(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, "Assign")
        lines += Graphvis_dot().linePair(p, myid)
        for node in n.nodes:
            lines += self.dispatch(node, myid)    
        lines += self.dispatch(n.expr, myid)
        return lines
    
    def visitDiscard(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, "Discard")
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.expr, myid)
        return lines

    def visitFunction(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("Function(%s)" % str(n.name)))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.code, myid)
        return lines
        
    # Expressions

    def visitConst(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("Const(%s)" % str(n.value)))
        lines += Graphvis_dot().linePair(p, myid)
        return lines

    def visitName(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("Name(%s)" % str(n.name)))
        lines += Graphvis_dot().linePair(p, myid)
        return lines

    def visitAssName(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("AssName(%s)" % str(n.name)))
        lines += Graphvis_dot().linePair(p, myid)
        return lines

    def visitList(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("List"))
        lines += Graphvis_dot().linePair(p, myid)
        for node in n.nodes:
            lines += self.dispatch(node, myid);
        return lines

    def visitDict(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("Dict"))
        lines += Graphvis_dot().linePair(p, myid)
        for item in n.items:
            lines += self.dispatch(item[1], myid);
        return lines

    def visitSubscript(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("Subscript"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.subs[0], myid)
        lines += self.dispatch(n.expr, myid)
        return lines
                
    def visitCompare(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.expr, myid)
        strops = []
        for op in n.ops:
            strops += [op[0]]
            lines += self.dispatch(op[1], myid)
        lines += Graphvis_dot().lineLabel(myid, ("Compare(%s)" % str(strops)))
        return lines

    def visitAdd(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("Add"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.left, myid)
        lines += self.dispatch(n.right, myid)
        return lines
   
    def visitOr(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("Or"))
        lines += Graphvis_dot().linePair(p, myid)
        for node in n.nodes:
            lines += self.dispatch(node, myid)
        return lines

    def visitAnd(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("And"))
        lines += Graphvis_dot().linePair(p, myid)
        for node in n.nodes:
            lines += self.dispatch(node, myid)
        return lines

    def visitNot(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("Not"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.expr, myid)
        return lines

    def visitUnarySub(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("UnarySub"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.expr, myid)
        return lines

    def visitIfExp(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("IfExp"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.test, myid)
        lines += self.dispatch(n.then, myid)
        lines += self.dispatch(n.else_, myid)
        return lines

    def visitIf(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("If"))
        lines += Graphvis_dot().linePair(p, myid)
        for (test,body) in n.tests:
            lines += self.dispatch(test, myid)
            lines += self.dispatch(body, myid)
        lines += self.dispatch(n.else_, myid)
        return lines

    def visitCallFunc(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("CallFunc"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.node, myid)
        for arg in n.args:
            lines += self.dispatch(arg, myid)
        return lines

    def visitReturn(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("Return"))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.value, myid)
        return lines

    def visitLambda(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("Lambda(%s)" % str(n.argnames)))
        lines += Graphvis_dot().linePair(p, myid)
        lines += self.dispatch(n.code, myid)
        return lines

    def visitWhile(self, n, p):
        lines = []
        myid = Graphvis_dot().uniqueid(n)
        lines += Graphvis_dot().lineLabel(myid, ("While"))
        lines += Graphvis_dot().linePair(p,myid)
        lines += self.dispatch(n.test, myid)
        lines += self.dispatch(n.body, myid)
        return lines
