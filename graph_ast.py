# Andy Sayler
# Fall 2012
# CU CS5525
# Python Compiler
# Visitor to graph an AST
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

import sys
import compiler

from compiler.ast import *

from vis import Visitor
from graphvis_dot import Graphvis_dot

class Graph_ast(Visitor):

    def writeGraph(self, ast, filepath):
        lines = self.preorder(ast)
        Graphvis_dot().drawGraph(lines, filepath)

    # Modules

    def visitModule(self, n):
        lines = []
        lines += Graphvis_dot().lineLabel(n, "Module")
        lines += self.dispatch(n.node, n)
        return lines
        
    # Statements    

    def visitStmt(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, "Stmt")
        lines += Graphvis_dot().linePair(p, n)
        for s in n.nodes:
            lines += self.dispatch(s, n)
        return lines
            
    def visitPrintnl(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, "Printnl")
        lines += Graphvis_dot().linePair(p, n)
        for node in n.nodes:
            lines += self.dispatch(node, n)
        return lines

    def visitAssign(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, "Assign")
        lines += Graphvis_dot().linePair(p, n)
        lines += self.dispatch(n.expr, n)
        return lines
    
    def visitDiscard(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, "Discard")
        lines += Graphvis_dot().linePair(p, n)
        lines += self.dispatch(n.expr, n)
        return lines
    
    # Expressions

    def visitConst(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("Const(%s)" % str(n.value)))
        lines += Graphvis_dot().linePair(p, n)
        return lines

    def visitName(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("Name(%s)" % str(n.name)))
        lines += Graphvis_dot().linePair(p, n)
        return lines

    def visitList(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("List"))
        lines += Graphvis_dot().linePair(p, n)
        for node in n.nodes:
            lines += self.dispatch(node, n);
        return lines

    def visitDict(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("Dict"))
        lines += Graphvis_dot().linePair(p, n)
        for item in n.items:
            lines += self.dispatch(item, n);
        return lines

    def visitSubscript(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("Subscript"))
        lines += Graphvis_dot().linePair(p, n)
        lines += self.dispatch(n.expr, n)
        return lines
                
    def visitCompare(self, n, p):
        lines = []
        lines += Graphvis_dot().linePair(p, n)
        lines += self.dispatch(n.expr, n)
        strops = []
        for op in n.ops:
            strops += [op[0]]
            lines += self.dispatch(op[1], n)
        lines += Graphvis_dot().lineLabel(n, ("Compare(%s)" % str(strops)))
        return lines

    def visitAdd(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("Add"))
        lines += Graphvis_dot().linePair(p, n)
        lines += self.dispatch(n.left, n)
        lines += self.dispatch(n.right, n)
        return lines
        
    def visitOr(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("Or"))
        lines += Graphvis_dot().linePair(p, n)
        for node in n.nodes:
            lines += self.dispatch(node, n)
        return lines

    def visitAnd(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("And"))
        lines += Graphvis_dot().linePair(p, n)
        for node in n.nodes:
            lines += self.dispatch(node, n)
        return lines

    def visitNot(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("Not"))
        lines += Graphvis_dot().linePair(p, n)
        lines += self.dispatch(n.expr, n)
        return lines

    def visitUnarySub(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("UnarySub"))
        lines += Graphvis_dot().linePair(p, n)
        lines += self.dispatch(n.expr, n)
        return lines

    def visitIfExp(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("IfExp"))
        lines += Graphvis_dot().linePair(p, n)
        lines += self.dispatch(n.test, n)
        lines += self.dispatch(n.then, n)
        lines += self.dispatch(n.else_, n)
        return lines

    def visitCallFunc(self, n, p):
        lines = []
        lines += Graphvis_dot().lineLabel(n, ("CallFunc"))
        lines += Graphvis_dot().linePair(p, n)
        lines += self.dispatch(n.node, n)
        for arg in n.args:
            lines += self.dispatch(arg)
        return lines
