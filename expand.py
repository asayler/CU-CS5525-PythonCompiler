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
        raise Exception("'Add' node no longer valid at this stage")

    def visitUnarySub(self, n):
        raise Exception("'UnarySub' node no longer valid at this stage")

    def visitNot(self, n):
        raise Exception("'Not' node no longer valid at this stage")

    def visitCompare(self, n):
        raise Exception("'Compare' node no longer valid at this stage")

    # Mono Type Nodes

    def visitmono_IsTag(self, n):
        if(n.typ == INT_t):
            return CallINJECTBOOL([CallISINT([self.dispatch(n.arg)])])
        elif(n.typ == BOOL_t):
            return CallINJECTBOOL([CallISBOOL([self.dispatch(n.arg)])])
        elif(n.typ == BIG_t):
            return CallINJECTBOOL([CallISBIG([self.dispatch(n.arg)])])
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

    # Mono Let and Subscript Assignment (Pass Through)

    def visitmono_Let(self, n):
        return mono_Let(self.dispatch(n.var), self.dispatch(n.rhs), self.dispatch(n.body))

    def visitmono_SubscriptAssign(self, n):
        return mono_SubscriptAssign(self.dispatch(n.target), self.dispatch(n.sub), self.dispatch(n.value))
    
    # Mono Expr Nodes
 
    def visitmono_IntAdd(self, n):
        return mono_IntAdd((self.dispatch(n.left), self.dispatch(n.right)), n.lineno)

    def visitmono_IntUnarySub(self, n):
        return mono_IntUnarySub(self.dispatch(n.expr), n.lineno)

    def visitmono_IntEqual(self, n):
        return mono_IntEqual((self.dispatch(n.left), self.dispatch(n.right)), n.lineno)

    def visitmono_IntNotEqual(self, n):
        return mono_IntNotEqual((self.dispatch(n.left), self.dispatch(n.right)), n.lineno)

    def visitmono_Dict(self, n):
        return mono_Dict(map(lambda (k,v): (self.dispatch(k), self.dispatch(v)), n.items), n.lineno)

    def visitmono_List(self, n):
        return mono_List(map(self.dispatch, n.nodes), n.lineno)

    def visitPrintnl(self, n):
        return Discard(CallPRINTANY([self.dispatch(n.nodes[0])]), n.lineno)

    def visitmono_IsTrue(self, n):
        return CallISTRUE([self.dispatch(n.expr)])

    def visitmono_Subscript(self, n):
        return CallGETSUB([self.dispatch(n.expr)] + map(self.dispatch, n.subs))

    # Explicate If
    def visitIfExp(self, n):
        return mono_IfExp(CallISTRUE([self.dispatch(n.test)]),
                          self.dispatch(n.then),
                          self.dispatch(n.else_)) 

    # Expand And/Or
    def AndToIfExp(self, nodes):
        if(len(nodes) < 2):
            # Error Condition
            raise Exception("expand: AND expression must have at least 2 nodes")
        
        thisnode = self.dispatch(nodes[0])
        
        if(len(nodes) == 2):
            # Exit Condition
            nextnode = self.dispatch(nodes[1])
            return mono_IfExp(CallISTRUE([thisnode]), nextnode, thisnode)
        else:
            # Recurse
            return mono_IfExp(CallISTRUE([thisnode]), self.AndToIfExp(nodes[1:]), thisnode)

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
            return mono_IfExp(CallISTRUE([thisnode]), thisnode, nextnode)
        else:
            # Recurse
            return mono_IfExp(CallISTRUE([thisnode]), thisnode, self.AndToIfExp(nodes[1:]))

    def visitOr(self, n):
        return self.OrToIfExp(n.nodes)
