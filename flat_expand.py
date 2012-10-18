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
from flatast import *

from unitcopy import CopyVisitor

# Helper Tools
from vis import Visitor
from functionwrappers import *

class FlatExpandVisitor(CopyVisitor):
    def visitmono_EmptyList(self, n):
        return CallMAKELIST([self.dispatch(n.length)])

    def visitmono_EmptyDict(self, n):
        return CallMAKEDICT([])

    def visitmono_SubscriptAssign(self, n):
        return Discard(CallSETSUB([self.dispatch(n.target), self.dispatch(n.sub), self.dispatch(n.value)]))

    def visitmono_IfExp(self, n):
        return mono_IfExp(self.dispatch(n.test), self.dispatch(n.then), self.dispatch(n.else_))

    def visitflat_InstrSeq(self, n):
        return flat_InstrSeq(map(self.dispatch, n.nodes), self.dispatch(n.expr))

    def visitmono_IntAdd(self, n):
        return mono_IntAdd((self.dispatch(n.left), self.dispatch(n.right)))

    def visitmono_IntEqual(self, n):
        return mono_IntEqual((self.dispatch(n.left), self.dispatch(n.right)))

    def visitmono_IntNotEqual(self, n):
        return mono_IntNotEqual((self.dispatch(n.left), self.dispatch(n.right)))

    def visitmono_IntUnarySub(self, n):
        return mono_IntUnarySub(self.dispatch(n.expr))
