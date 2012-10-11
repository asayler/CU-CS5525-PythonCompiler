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

class Graph_ast(Visitor):

    digraphOpen = "digraph G {"
    digraphClose = "}"
    attrOpen = "["
    attrClose = "]"
    attrLabel = "label="
    arrow = " -> "
    qt = '\"'
    sc = ';'
    nl = '\n'
    tb = '\t'
    nltb = nl + tb

    def linePair(self, parent, child):
        pid = self.qt + str(id(parent)) + self.qt
        cid = self.qt + str(id(child))  + self.qt
        return [(pid + self.arrow + cid + self.sc)]

    def lineLabel(self, n, label):
        nid = self.qt + str(id(n)) + self.qt        
        return [(nid + " " +
                 self.attrOpen + self.attrLabel +
                 self.qt + label + self.qt +
                 self.attrClose + self.sc)]

    def drawGraph(self, ast, filepath):
        lines = self.preorder(ast)
        graph = (self.digraphOpen + self.nltb +
                 self.nltb.join(lines) +
                 self.nl + self.digraphClose)
        outputfile = open(filepath, 'w+')
        outputfile.write(graph + self.nl)
        outputfile.close()

    # Modules

    def visitModule(self, n):
        lines = []
        lines += self.lineLabel(n, "Module")
        lines += self.dispatch(n.node, n)
        return lines
        
    # Statements    

    def visitStmt(self, n, p):
        lines = []
        lines += self.lineLabel(n, "Stmt")
        lines += self.linePair(p, n)
        for s in n.nodes:
            lines += self.dispatch(s, n)
        return lines
            
    def visitPrintnl(self, n, p):
        lines = []
        lines += self.lineLabel(n, "Printnl")
        lines += self.linePair(p, n)
        for node in n.nodes:
            lines += self.dispatch(node, n)
        return lines

    def visitAssign(self, n, p):
        lines = []
        lines += self.lineLabel(n, "Assign")
        lines += self.linePair(p, n)
        lines += self.dispatch(n.expr, n)
        return lines
    
    def visitDiscard(self, n, p):
        lines = []
        lines += self.lineLabel(n, "Discard")
        lines += self.linePair(p, n)
        lines += self.dispatch(n.expr, n)
        return lines
    
    # Expressions

    def visitConst(self, n, p):
        lines = []
        lines += self.lineLabel(n, ("Const(%s)" % str(n.value)))
        lines += self.linePair(p, n)
        return lines

    def visitName(self, n, p):
        lines = []
        lines += self.lineLabel(n, ("Name(%s)" % str(n.name)))
        lines += self.linePair(p, n)
        return lines

    def visitList(self, n, p):
        lines = []
        lines += self.lineLabel(n, ("List"))
        lines += self.linePair(p, n)
        for node in n.nodes:
            lines += self.dispatch(node, n);
        return lines

    def visitDict(self, n, p):
        lines = []
        lines += self.lineLabel(n, ("Dict"))
        lines += self.linePair(p, n)
        for item in n.items:
            lines += self.dispatch(item, n);
        return lines

    def visitSubscript(self, n, p):
        lines = []
        lines += self.lineLabel(n, ("Subscript"))
        lines += self.linePair(p, n)
        lines += self.dispatch(n.expr, n)
        return lines
                
    def visitCompare(self, n, p):
        lines = []
        lines += self.linePair(p, n)
        lines += self.dispatch(n.expr, n)
        strops = []
        for op in n.ops:
            strops += [op[0]]
            lines += self.dispatch(op[1], n)
        lines += self.lineLabel(n, ("Compare(%s)" % str(strops)))
        return lines

    def visitAdd(self, n, p):
        lines = []
        lines += self.lineLabel(n, ("Add"))
        lines += self.linePair(p, n)
        lines += self.dispatch(n.left, n)
        lines += self.dispatch(n.right, n)
        return lines
        
    def visitOr(self, n, p):
        lines = []
        lines += self.lineLabel(n, ("Or"))
        lines += self.linePair(p, n)
        for node in n.nodes:
            lines += self.dispatch(node, n)
        return lines

    def visitAnd(self, n, p):
        lines = []
        lines += self.lineLabel(n, ("And"))
        lines += self.linePair(p, n)
        for node in n.nodes:
            lines += self.dispatch(node, n)
        return lines

    def visitNot(self, n, p):
        lines = []
        lines += self.lineLabel(n, ("Not"))
        lines += self.linePair(p, n)
        lines += self.dispatch(n.expr, n)
        return lines

    def visitUnarySub(self, n, p):
        lines = []
        lines += self.lineLabel(n, ("UnarySub"))
        lines += self.linePair(p, n)
        lines += self.dispatch(n.expr, n)
        return lines

    def visitIfExp(self, n, p):
        lines = []
        lines += self.lineLabel(n, ("IfExp"))
        lines += self.linePair(p, n)
        lines += self.dispatch(n.test, n)
        lines += self.dispatch(n.then, n)
        lines += self.dispatch(n.else_, n)
        return lines

    def visitCallFunc(self, n, p):
        lines = []
        lines += self.lineLabel(n, ("CallFunc"))
        lines += self.linePair(p, n)
        lines += self.dispatch(n.node, n)
        for arg in n.args:
            lines += self.dispatch(arg)
        return lines
