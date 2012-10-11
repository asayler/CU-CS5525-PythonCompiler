# Andy Sayler
# Fall 2012
# CU CS5525
# Python Compiler
# Visitor to walk and name an AST
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

class Walk_ast(Visitor):

    # Modules

    def visitModule(self, n):
        sys.stderr.write("Visited Module...\n")
        self.dispatch(n.node)

    # Statements    

    def visitStmt(self, n):
        sys.stderr.write("Visited Stmt...\n")
        for s in n.nodes:
            self.dispatch(s)

    def visitPrintnl(self, n):
        sys.stderr.write("Visited Printnl...\n")
        for node in n.nodes:
            self.dispatch(node)

    def visitAssign(self, n):
        sys.stderr.write("Visited Assign...\n")
        self.dispatch(n.expr)
    
    def visitDiscard(self, n):
        sys.stderr.write("Visited Discard...\n")
        self.dispatch(n.expr)
    
    # Expressions

    def visitConst(self, n):
        sys.stderr.write("Visited Const...\n")

    def visitName(self, n):
        sys.stderr.write("Visited Name...\n")

    def visitList(self, n):
        sys.stderr.write("Visited List...\n")
        for node in n.nodes:
            self.dispatch(node);

    def visitDict(self, n):
        sys.stderr.write("Visited Dict...\n")
        for item in n.items:
            self.dispatch(item);

    def visitSubscript(self, n):
        sys.stderr.write("Visited Subscript...\n")
        self.dispatch(n.expr)
        
    def visitCompare(self, n):
        sys.stderr.write("Visited Compare...\n")
        self.dispatch(n.expr)
        for op in n.ops:
            self.dispatch(op[1])

    def visitAdd(self, n):
        sys.stderr.write("Visited Add...\n")
        self.dispatch(n.left)
        self.dispatch(n.right)
        
    def visitOr(self, n):
        sys.stderr.write("Visited Or...\n")
        for node in n.nodes:
            self.dispatch(node)

    def visitAnd(self, n):
        sys.stderr.write("Visited And...\n")
        for node in n.nodes:
            self.dispatch(node)

    def visitNot(self, n):
        sys.stderr.write("Visited Not...\n")
        self.dispatch(n.expr)

    def visitUnarySub(self, n):
        sys.stderr.write("Visited UnarySub...\n")
        self.dispatch(n.expr)

    def visitIfExp(self, n):
        sys.stderr.write("Visited IfExp...\n")
        self.dispatch(n.test)
        self.dispatch(n.then)
        self.dispatch(n.else_)

    def visitCallFunc(self, n):
        sys.stderr.write("Visited CallFunc...\n")
        self.dispatch(n.node)
        for arg in n.args:
            self.dispatch(arg)
