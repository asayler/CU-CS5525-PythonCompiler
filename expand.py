# CU CS5525
# Fall 2012
# Python Compiler
#
# expand.py
# Visitor Functions to Expand AST
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

# Data Types
from compiler.ast import *
from monoast import *

from unitcopy import CopyVisitor

# Helper Tools
from vis import Visitor
from functionwrappers import *

class ExpandVisitor(CopyVisitor):
    def __init__(self):
        super(ExpandVisitor,self).__init__()
        CopyVisitor.visitModule = visitModulePostCC
        CopyVisitor.visitSLambdaLabel = SLambdaLabel.visitSLambdaLabel
        CopyVisitor.visitIndirectCallFunc = IndirectCallFunc.visitIndirectCallFunc

    def visitIsTag(self, n):
        if(n.typ == INT_t):
            return CallINJECTBOOL([CallISINT([self.dispatch(n.arg)])])
        elif(n.typ == BOOL_t):
            return CallINJECTBOOL([CallISBOOL([self.dispatch(n.arg)])])
        elif(n.typ == BIG_t):
            return CallINJECTBOOL([CallISBIG([self.dispatch(n.arg)])])
        else:
            raise Exception("expand: IsTag - unknown type %s" % str(n.typ))
    
    def visitProjectTo(self, n):
        if(n.typ == INT_t):
            return CallPROJECTINT([self.dispatch(n.arg)])
        elif(n.typ == BOOL_t):
            return CallPROJECTBOOL([self.dispatch(n.arg)])
        elif(n.typ == BIG_t):
            return CallPROJECTBIG([self.dispatch(n.arg)])
        else:
            raise Exception("expand: ProjectTo - unknown type %s" % str(n.typ))
    
    def visitInjectFrom(self, n):
        if(n.typ == INT_t):
            return CallINJECTINT([self.dispatch(n.arg)])
        elif(n.typ == BOOL_t):
            return CallINJECTBOOL([self.dispatch(n.arg)])
        elif(n.typ == BIG_t):
            return CallINJECTBIG([self.dispatch(n.arg)])
        else:
            raise Exception("expand: InjectFrom - unknown type %s" % str(n.typ))
        
    def visitPrintnl(self, n):
        return Discard(CallPRINTANY([self.dispatch(n.nodes[0])]), n.lineno)

    def visitSubscriptAssign(self, n):
        return Discard(CallSETSUB([self.dispatch(n.target),
                                   self.dispatch(n.sub),
                                   self.dispatch(n.value)]))
    
    def visitSubscript(self, n):
        return CallGETSUB([self.dispatch(n.expr),
                           self.dispatch(n.subs[0])])

    # Explicate If
    def visitIfExp(self, n):
        return IfExp(CallISTRUE([self.dispatch(n.test)]),
                     self.dispatch(n.then),
                     self.dispatch(n.else_)) 
    # Explicate While
    def visitWhile(self, n):
        return While(CallISTRUE([self.dispatch(n.test)]),
                     self.dispatch(n.body),
                     n.else_) 

    # Expand And/Or
    def AndToIfExp(self, nodes):
        if(len(nodes) < 2):
            # Error Condition
            raise Exception("expand: AND expression must have at least 2 nodes")
        
        thisnode = self.dispatch(nodes[0])
        
        if(len(nodes) == 2):
            # Exit Condition
            nextnode = self.dispatch(nodes[1])
            return IfExp(CallISTRUE([thisnode]), nextnode, thisnode)
        else:
            # Recurse
            return IfExp(CallISTRUE([thisnode]), self.AndToIfExp(nodes[1:]), thisnode)

    def visitAnd(self, n):
        return self.AndToIfExp(n.nodes)
    
    def OrToIfExp(self, nodes):
        if(len(nodes) < 2):
            # Error Condition
            raise Exception("expand: OR expression must have at least 2 nodes")
        
        thisnode = self.dispatch(nodes[0])
        
        if(len(nodes) == 2):
            # Exit Condition
            nextnode = self.dispatch(nodes[1])
            return IfExp(CallISTRUE([thisnode]), thisnode, nextnode)
        else:
            # Recurse
            return IfExp(CallISTRUE([thisnode]), thisnode, self.AndToIfExp(nodes[1:]))

    def visitOr(self, n):
        return self.OrToIfExp(n.nodes)
