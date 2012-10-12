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

# Data Types
from compiler.ast import *
from monoast import *

# Flatten expressions to 3-address instructions (Remove Complex Operations)

# Input: an AST for P_1
# Output: an AST for P_1 (put without complex operations)

# Notes: this introduces too many variables and moves, but that's OK.
# Register allocation with move biasing will hopefully take care of it.

def make_assign(lhs, rhs):
    return Assign(nodes=[AssName(name=lhs, flags='OP_ASSIGN')], expr=rhs)

class FlattenVisitor(CopyVisitor):

    # Banned Nodes

    def visitPrintnl(self, n):
        raise Exception("AST 'Printnl' node no longer valid at this stage")

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

    def visitmono_Add(self, n, needs_to_be_simple):
        (left, ss1) = self.dispatch(n.left, True)
        (right, ss2) = self.dispatch(n.right, True)
        if needs_to_be_simple:
            tmp = generate_name('tmp')
            return (Name(tmp), ss1 + ss2 + [make_assign(tmp, Add((left, right)))])
        else:
            return (Add((left, right)), ss1 + ss2)            

    def visitUnarySub(self, n, needs_to_be_simple):
        (expr,ss) = self.dispatch(n.expr, True)
        if needs_to_be_simple:
            tmp = generate_name('tmp')
            return (Name(tmp), ss + [make_assign(tmp, UnarySub(expr))])
        else:
            return (UnarySub(expr), ss)

    def visitCallFunc(self, n, needs_to_be_simple):
        if isinstance(n.node, Name):
            args_sss = [self.dispatch(arg, True) for arg in n.args]
            args = [arg for (arg,ss) in args_sss]
            ss = reduce(lambda a,b: a + b, [ss for (arg,ss) in args_sss], [])
            if needs_to_be_simple:
                tmp = generate_name('tmp')
                return (Name(tmp), ss + [make_assign(tmp, CallFunc(n.node, args))])
            else:
                return (CallFunc(n.node, args), ss)
        else:
            raise Exception('flatten: only calls to named functions allowed')