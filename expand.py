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

    def visitAdd(self, n, p):
        raise Exception("AST 'Add' node no longer valid at this stage")

    # Mono Type Nodes
    
    def visitmono_ProjectTo(self, n):
        if(n.typ == INT_t):
            return CallPROJECTINT(n.arg)
        elif(n.typ == BOOL_t):
            return CallPROJECTBOOL(n.arg)
        elif(n.typ == BIG_t):
            return CallPROJECTBIG(n.arg)
        else:
            raise Exception("expand: ProjectTo - unknown type %s" % str(n.typ))
    
    def visitmono_InjectFrom(self, n):
        if(n.typ == INT_t):
            return CallINJECTINT(n.arg)
        elif(n.typ == BOOL_t):
            return CallINJECTBOOL(n.arg)
        elif(n.typ == BIG_t):
            return CallINJECTBIG(n.arg)
        else:
            raise Exception("expand: InjectFrom - unknown type %s" % str(n.typ))
       
    # Mono Expr Nodes

    def visitmono_Add(self, n):
        return mono_Add((self.dispatch(n.left), self.dispatch(n.right)), n.lineno)
    
