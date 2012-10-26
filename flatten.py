# CU CS5525
# Fall 2012
# Python Compiler
#
# flatten.py
# Visitor Funstions to Flatten AST
#
# Adopted from code by Jeremy Siek, Fall 2012
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

# Helper Types
from vis import Visitor

# Helper Tools
from utilities import generate_name, make_assign
from unitcopy import CopyVisitor

from functionwrappers import *

# Data Types
from compiler.ast import *
from monoast import *

# Flatten expressions to 3-address instructions (Remove Complex Operations)

# Input: an AST for P_1
# Output: an AST for P_1 (put without complex operations)

# Notes: this introduces too many variables and moves, but that's OK.
# Register allocation with move biasing will hopefully take care of it.

class FlattenVisitor(CopyVisitor):
    def __init__(self):
        super(FlattenVisitor,self).__init__()
        del CopyVisitor.visitPrintnl
        del CopyVisitor.visitIsTag
        del CopyVisitor.visitProjectTo
        del CopyVisitor.visitInjectFrom
        del CopyVisitor.visitAnd
        del CopyVisitor.visitOr
        del CopyVisitor.visitSubscript
        del CopyVisitor.visitSubscriptAssign

    # For statements: takes a statement and returns a list of instructions

    def visitStmt(self, n):
        sss  = []
        for s in n.nodes:
            sss += [self.dispatch(s)]
        return Stmt(reduce(lambda a,b: a + b, sss, []), n.lineno)

    def visitAssign(self, n):
        myss = []
        (rhs, ss) = self.dispatch(n.expr, False)
        myss += ss
        myss += [Assign(n.nodes, rhs)]
        return myss

    def visitDiscard(self, n):
        (e, ss) = self.dispatch(n.expr, True)
        return ss

    def visitReturn(self, n):
        (e, ss) = self.dispatch(n.value, True)
        return ss + [Return(e)]

    # For expressions: takes an expression and a bool saying whether the
    # expression needs to be simple, and returns an expression
    # (a Name or Const if it needs to be simple) and a list of instructions.

    def visitConst(self, n, needs_to_be_simple):
        return (n, [])

    def visitName(self, n, needs_to_be_simple):
        return (n, [])

    def visitSLambdaLabel(self, n, needs_to_be_simple):
        return (n, [])

    def visitLet(self, n, needs_to_be_simple):
        (rhs, ss1) = self.dispatch(n.rhs, True)
        (body, ss2) = self.dispatch(n.body, True)
        return (body, ss1 + [make_assign(n.var.name, rhs)] + ss2)

    def visitIntAdd(self, n, needs_to_be_simple):
        (left, ss1) = self.dispatch(n.left, True)
        (right, ss2) = self.dispatch(n.right, True)
        if needs_to_be_simple:
            tmp = generate_name('intaddtmp')
            return (Name(tmp), ss1 + ss2 + [make_assign(tmp, IntAdd((left, right)))])
        else:
            return (IntAdd((left, right)), ss1 + ss2)

    def visitIntEqual(self, n, needs_to_be_simple):
        (left, ss1) = self.dispatch(n.left, True)
        (right, ss2) = self.dispatch(n.right, True)
        if needs_to_be_simple:
            tmp = generate_name('intequaltmp')
            return (Name(tmp), ss1 + ss2 + [make_assign(tmp, IntEqual((left, right)))])
        else:
            return (IntEqual((left, right)), ss1 + ss2)

    def visitIntNotEqual(self, n, needs_to_be_simple):
        (left, ss1) = self.dispatch(n.left, True)
        (right, ss2) = self.dispatch(n.right, True)
        if needs_to_be_simple:
            tmp = generate_name('intnotequaltmp')
            return (Name(tmp), ss1 + ss2 + [make_assign(tmp, IntNotEqual((left, right)))])
        else:
            return (IntNotEqual((left, right)), ss1 + ss2)

    def visitIntUnarySub(self, n, needs_to_be_simple):
        (expr,ss) = self.dispatch(n.expr, True)
        if needs_to_be_simple:
            tmp = generate_name('usubtmp')
            return (Name(tmp), ss + [make_assign(tmp, IntUnarySub(expr))])
        else:
            return (IntUnarySub(expr), ss)

    def visitIndirectCallFunc(self, n, needs_to_be_simple):
        if isinstance(n.node, CallFunc):
            args_sss = [self.dispatch(arg, True) for arg in n.args]
            args = [arg for (arg,ss) in args_sss]
            ss = reduce(lambda a,b: a + b, [ss for (arg,ss) in args_sss], [])
            (expr, sss) = self.dispatch(n.node, True)
            ss += sss
            if needs_to_be_simple:
                tmp = generate_name('indirectcallfunctmp')
                return (Name(tmp), ss + [make_assign(tmp, IndirectCallFunc(expr, args))])
            else:
                return (IndirectCallFunc(expr, args), ss)
        else:
            raise Exception('flatten: only indirectcalls to closure converted functions allowed')

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
            raise Exception('flatten: only calls to named functions allowed, tried to call %s:%s' % (n.node, n.node.__class__))

    def visitIfExp(self, n, needs_to_be_simple):
        (teste, testss) = self.dispatch(n.test, True)
        (thene, thenss) = self.dispatch(n.then, True)
        (elsee, elsess) = self.dispatch(n.else_, True)
        simple = IfExp(teste,
                       InstrSeq(thenss, thene),
                       InstrSeq(elsess, elsee))
        if needs_to_be_simple:
            tmp = generate_name('ifexptmp')
            myexpr = (Name(tmp))
            myss = [make_assign(tmp, simple)]
        else:
            myexpr = simple
            myss = []
        return (myexpr, testss + myss)

    def visitList(self, n, needs_to_be_simple):
        myss = []
        # Create new list
        ll = len(n.nodes)
        (expr, ss) = self.dispatch(CallINJECTBIG([CallMAKELIST([CallINJECTINT([Const(ll)])])]),
                                   needs_to_be_simple)
        myss += ss
        # Add each list memeber
        cnt = 0
        for node in n.nodes:
            myss += self.dispatch(Discard(CallSETSUB([expr, CallINJECTINT([Const(cnt)]), node])))
            cnt += 1
        return (expr, myss)

    def visitDict(self, n, needs_to_be_simple):
        myss = []
        # Create new Dict
        (expr, ss) = self.dispatch(CallINJECTBIG([CallMAKEDICT([])]), needs_to_be_simple)
        myss += ss
        # Add each dict memeber
        for item in n.items:
            myss += self.dispatch(Discard(CallSETSUB([expr, item[0], item[1]])))            
        return (expr, myss)
