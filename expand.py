#!/usr/bin/python

# Andy Sayler
# Fall 2012
# CU CS5525
# expand visitor functions
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

import sys

# Data Types
from compiler.ast import *
from monoast import *

from unitcopy import CopyVisitor

# Helper Tools
from vis import Visitor
from functionwrappers import *

class ExpandVisitor(CopyVisitor):

    # Banned Nodes

    def visitAdd(self, n):
        raise Exception("AST 'Add' node no longer valid at this stage")

    # Mono Type Nodes

    def visitmono_IsTag(self, n):
        if(n.typ == INT_t):
            return CallISINT([self.dispatch(n.arg)])
        elif(n.typ == BOOL_t):
            return CallISBOOL([self.dispatch(n.arg)])
        elif(n.typ == BIG_t):
            return CallISBIG([self.dispatch(n.arg)])
        else:
            raise Exception("expand: IsTag - unknown type %s" % str(n.typ))
    
    def visitmono_ProjectTo(self, n):
        if(n.typ == INT_t):
            return CallPROJECTINT([self.dispatch(n.arg)])
        elif(n.typ == BOOL_t):
            return CallPROJECTBOOL([self.dispatch(n.arg)])
        elif(n.typ == BIG_t):
            return CallPROJECTBIG([self.dispatch(n.arg)])
        else:
            raise Exception("expand: ProjectTo - unknown type %s" % str(n.typ))
    
    def visitmono_InjectFrom(self, n):
        if(n.typ == INT_t):
            return CallINJECTINT([self.dispatch(n.arg)])
        elif(n.typ == BOOL_t):
            return CallINJECTBOOL([self.dispatch(n.arg)])
        elif(n.typ == BIG_t):
            return CallINJECTBIG([self.dispatch(n.arg)])
        else:
            raise Exception("expand: InjectFrom - unknown type %s" % str(n.typ))


    # Mono Let (Pass Through)

    def visitmono_Let(self, n):
        return mono_Let(self.dispatch(n.var), self.dispatch(n.rhs), self.dispatch(n.body));
        
    # Mono Expr Nodes
 
    def visitmono_IntAdd(self, n):
        return mono_IntAdd((self.dispatch(n.left),self.dispatch(n.right)), n.lineno)

    def visitPrintnl(self, n):
        return Discard(CallPRINTANY([self.dispatch(n.nodes[0])]), n.lineno)

    # And/Or
    def AndToIfExp(self, nodes):
        if(len(nodes) < 2):
            # Error Condition
            raise Exception("expand: AND expression must have at least 2 nodes")
        
        thisnode = self.dispatch(nodes[0])
        
        if(len(nodes) == 2):
            # Exit Condition
            nextnode = self.dispatch(nodes[1])
            return IfExp(thisnode, nextnode, thisnode)
        else:
            # Recurse
            return IfExp(thisnode, self.AndToIfExp(nodes[1:]), thisnode)

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
            return IfExp(thisnode, thisnode, nextnode)
        else:
            # Recurse
            return IfExp(thisnode, thisnode, self.AndToIfExp(nodes[1:]))

    def visitOr(self, n):
        return self.OrToIfExp(n.nodes)
        
