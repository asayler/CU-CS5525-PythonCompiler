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

    def visitModule(self, n):
        sys.stderr.write("Visited Module...\n")
        self.dispatch(n.node)

    def visitStmt(self, n):
        sys.stderr.write("Visited Stmt...\n")
        for s in n.nodes:
            self.dispatch(s)

    def visitPrintnl(self, n):
        sys.stderr.write("Visited Printnl...\n")
        self.dispatch(n.nodes[0])

    def visitAssign(self, n):
        sys.stderr.write("Visited Assign...\n")
        self.dispatch(n.expr)
    
    def visitDiscard(self, n):
        sys.stderr.write("Visited Discard...\n")
        self.dispatch(n.expr)
    
    def visitConst(self, n):
        sys.stderr.write("Visited Const...\n")

    def visitName(self, n):
        sys.stderr.write("Visited Name...\n")

    def visitAdd(self, n):
        sys.stderr.write("Visited Add...\n")
        self.dispatch(n.left)
        self.dispatch(n.right)
        
    def visitUnarySub(self, n):
        sys.stderr.write("Visited UnarySub...\n")
        self.dispatch(n.expr)

    def visitCallFunc(self, n):
        sys.stderr.write("Visited CallFunc...\n")
        self.dispatch(n.node)
        for arg in n.args:
            self.dispatch(arg, True)
