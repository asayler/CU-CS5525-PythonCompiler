# CU CS5525
# Fall 2012
# GSV Python Compiler
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
#    Andrew (Andy) Sayler
#       http://www.andysayler.com
#    Michael (Mike) Vitousek
#       http://csel.cs.colorado.edu/~mivi2269/
#
# Copyright (c) 2012 by Anne Gatchell, Andy Sayler, and Mike Vitousek
#
# This file is part of the GSV CS5525 Fall 2012 Python Compiler.
#
#    The GSV CS5525 Fall 2012 Python Compiler is free software: you
#    can redistribute it and/or modify it under the terms of the GNU
#    General Public License as published by the Free Software
#    Foundation, either version 3 of the License, or (at your option)
#    any later version.
#
#    The GSV CS5525 Fall 2012 Python Compiler is distributed in the
#    hope that it will be useful, but WITHOUT ANY WARRANTY; without
#    even the implied warranty of MERCHANTABILITY or FITNESS FOR A
#    PARTICULAR PURPOSE.  See the GNU General Public License for more
#    details.
#
#    You should have received a copy of the GNU General Public License
#    along with the GSV CS5525 Fall 2012 Python Compiler.  If not, see
#    <http://www.gnu.org/licenses/>.

# Data Types
from pyast import *

# Parents
from list_visitor import ListVisitor

# Helper Tools
from utilities import generate_name, make_assign
from functionwrappers import *

class FlattenVisitor(ListVisitor):

    def __init__(self):
        super(FlattenVisitor,self).__init__()

    # For statements: takes a statement and returns a list of instructions

    def visitVarAssign(self, n, *args):
        myss = []
        (rhs, ss) = self.dispatch(n.value, False)
        myss += ss
        myss += [VarAssign(n.target, rhs)]
        return myss

    def visitWhile(self, n, *args):
        teste, testss = self.dispatch(n.test, True)
        bodyss = self.dispatch(n.body, True)
        elsess = self.dispatch(n.else_, True) if n.else_ else None
        return [WhileFlat(StmtList(testss), teste, bodyss, elsess)]

    def visitDiscard(self, n, *args):
        (e, ss) = self.dispatch(n.expr, True)
        return ss

    # For expressions: takes an expression and a bool saying whether the
    # expression needs to be simple, and returns an expression
    # (a Name or Const if it needs to be simple) and a list of instructions.

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

    def visitIntCmp(self, n, needs_to_be_simple):
        (left, ss1) = self.dispatch(n.left, True)
        (right, ss2) = self.dispatch(n.right, True)
        if needs_to_be_simple:
            tmp = generate_name('intequaltmp')
            return (Name(tmp), ss1 + ss2 + [make_assign(tmp, IntCmp(n.op, (left, right)))])
        else:
            return (IntCmp(n.op, (left, right)), ss1 + ss2)

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
            raise Exception('flatten: only calls to named functions allowed,' 
                            'tried to call %s:%s' % (n.node, n.node.__class__))

    def visitIfExp(self, n, needs_to_be_simple):
        (teste, testss) = self.dispatch(n.test, True)
        (thene, thenss) = self.dispatch(n.then, True)
        (elsee, elsess) = self.dispatch(n.else_, True)
        simple = IfExpFlat(teste,
                       InstrSeq(StmtList(thenss), thene),
                       InstrSeq(StmtList(elsess), elsee))
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
            valname = generate_name('item')
            myss += self.dispatch(Discard(Let(Name(valname),
                                              item[1],
                                              CallSETSUB([expr, item[0], Name(valname)]))))   
        return (expr, myss)
