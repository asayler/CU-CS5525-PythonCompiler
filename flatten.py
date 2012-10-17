#!/usr/bin/python

# Andy Sayler
# Fall 2012
# CU CS5525
# flatten visitor functions
#
# Adopted from Jeremy Siek, Fall 2012
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

# Helper Types
from vis import Visitor

# Helper Tools
from utilities import generate_name
from unitcopy import CopyVisitor

from functionwrappers import *

# Data Types
from compiler.ast import *
from monoast import *
from flatast import *

# Flatten expressions to 3-address instructions (Remove Complex Operations)

# Input: an AST for P_1
# Output: an AST for P_1 (put without complex operations)

# Notes: this introduces too many variables and moves, but that's OK.
# Register allocation with move biasing will hopefully take care of it.

def make_assign(lhs, rhs):
    return Assign(nodes=[AssName(name=lhs, flags='OP_ASSIGN')], expr=rhs)

class FlattenVisitor(CopyVisitor):

    # Banned Nodes

    def visitAdd(self, n):
        raise Exception("'Add' node no longer valid at this stage")

    def visitUnarySub(self, n):
        raise Exception("'UnarySub' node no longer valid at this stage")

    def visitNot(self, n):
        raise Exception("'Not' node no longer valid at this stage")

    def visitCompare(self, n):
        raise Exception("'Compare' node no longer valid at this stage")

    def visitPrintnl(self, n):
        raise Exception("'Printnl' node no longer valid at this stage")

    def visitmono_IsTag(self, n):
        raise Exception("'mono_IsTag' node no longer valid at this stage")

    def visitmono_ProjectTo(self, n):
        raise Exception("'mono_ProjectTo' node no longer valid at this stage")

    def visitmono_InjectFrom(self, n):
        raise Exception("'mono_InjectFrom' node no longer valid at this stage")

    def visitAnd(self, n):
        raise Exception("'And' node no longer valid at this stage")

    def visitOr(self, n):
        raise Exception("'Or' node no longer valid at this stage")

    def mono_IsTrue(self, n):
        raise Exception("'mono_IsTrue' node no longer valid at this stage")

    def IfExp(self, n):
        raise Exception("'IfExp' node no longer valid at this stage")

    # For statements: takes a statement and returns a list of instructions

    def visitStmt(self, n):
        sss  = []
        for s in n.nodes:
            sss += [self.dispatch(s)]
        return Stmt(reduce(lambda a,b: a + b, sss, []), n.lineno)

    def visitAssign(self, n):
        (rhs,ss) = self.dispatch(n.expr, False)
        return ss + [Assign(n.nodes, rhs)]

    def visitDiscard(self, n):
        (e, ss) = self.dispatch(n.expr, True)
        return ss

    # For expressions: takes an expression and a bool saying whether the
    # expression needs to be simple, and returns an expression
    # (a Name or Const if it needs to be simple) and a list of instructions.

    def visitConst(self, n, needs_to_be_simple):
        return (n, [])

    def visitName(self, n, needs_to_be_simple):
        return (n, [])

    def visitmono_Let(self, n, needs_to_be_simple):
        (rhs, ss1) = self.dispatch(n.rhs, True)
        (body, ss2) = self.dispatch(n.body, True)
        return (body, ss1 + [make_assign(n.var.name, rhs)] + ss2)

    def visitmono_IntAdd(self, n, needs_to_be_simple):
        (left, ss1) = self.dispatch(n.left, True)
        (right, ss2) = self.dispatch(n.right, True)
        if needs_to_be_simple:
            tmp = generate_name('intaddtmp')
            return (Name(tmp), ss1 + ss2 + [make_assign(tmp, mono_IntAdd((left, right)))])
        else:
            return (mono_IntAdd((left, right)), ss1 + ss2)

    def visitmono_IntEqual(self, n, needs_to_be_simple):
        (left, ss1) = self.dispatch(n.left, True)
        (right, ss2) = self.dispatch(n.right, True)
        if needs_to_be_simple:
            tmp = generate_name('intequaltmp')
            return (Name(tmp), ss1 + ss2 + [make_assign(tmp, mono_IntEqual((left, right)))])
        else:
            return (mono_IntEqual((left, right)), ss1 + ss2)

    def visitmono_IntNotEqual(self, n, needs_to_be_simple):
        (left, ss1) = self.dispatch(n.left, True)
        (right, ss2) = self.dispatch(n.right, True)
        if needs_to_be_simple:
            tmp = generate_name('intnotequaltmp')
            return (Name(tmp), ss1 + ss2 + [make_assign(tmp, mono_IntNotEqual((left, right)))])
        else:
            return (mono_IntNotEqual((left, right)), ss1 + ss2)

    def visitmono_IntUnarySub(self, n, needs_to_be_simple):
        (expr,ss) = self.dispatch(n.expr, True)
        if needs_to_be_simple:
            tmp = generate_name('usubtmp')
            return (Name(tmp), ss + [make_assign(tmp, mono_IntUnarySub(expr))])
        else:
            return (mono_IntUnarySub(expr), ss)

    def visitCallFunc(self, n, needs_to_be_simple):
        if isinstance(n.node, Name):
            args_sss = [self.dispatch(arg, True) for arg in n.args]
            args = [arg for (arg,ss) in args_sss]
            ss = reduce(lambda a,b: a + b, [ss for (arg,ss) in args_sss], [])
            if needs_to_be_simple:
                tmp = generate_name('callfunctmp')
                return (Name(tmp), ss + [make_assign(tmp, CallFunc(n.node, args))])
            else:
                return (CallFunc(n.node, args), ss)
        else:
            raise Exception('flatten: only calls to named functions allowed')

    def visitmono_IfExp(self, n, needs_to_be_simple):
        (teste, testss) = self.dispatch(n.test, True)
        (thene, thenss) = self.dispatch(n.then, True)
        (elsee, elsess) = self.dispatch(n.else_, True)
        simple = mono_IfExp(teste,
                            flat_InstrSeq(thenss, thene),
                            flat_InstrSeq(elsess, elsee))
        if needs_to_be_simple:
            tmp = generate_name('ifexptmp')
            myexpr = (Name(tmp))
            myss = [make_assign(tmp, simple)]
        else:
            myexpr = simple
            myss = []
        return (myexpr, testss + myss)
