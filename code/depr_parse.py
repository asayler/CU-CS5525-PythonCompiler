# CU CS5525
# Fall 2012
# GSV Python Compiler
#
# depr_parse.py
# Depricated "compiler" module parse infrastructure
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

import compiler
from compiler.ast import *
import pyast
from vis import *

def parse(inputFilePath):
    parsedast = compiler.parseFile(inputFilePath)
    return ParseConvert().preorder(parsedast)

class ParseConvert(Visitor):
    def visitModule(self, n):
        return pyast.Module(self.dispatch(n.node))
    
    def visitClass(self, n):
        return pyast.Class(n.name, map(self.dispatch, n.bases), 
                     self.dispatch(n.code))

    def visitStmt(self, n):
        nodes = []
        for s in n.nodes:
            nodes += [self.dispatch(s)]
        return pyast.StmtList(nodes)

    def visitPrintnl(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return pyast.Discard(pyast.CallFunc(pyast.Name('print_any'), nodes))

    def visitAssign(self, n):
        if isinstance(n.nodes[0], Subscript):
            return pyast.SubscriptAssign(self.dispatch(n.nodes[0].expr), 
                                         map(self.dispatch, n.nodes[0].subs),
                                         self.dispatch(n.expr))
        elif isinstance(n.nodes[0], AssAttr):
            return pyast.AttrAssign(self.dispatch(n.nodes[0].expr), 
                                    n.nodes[0].attrname,
                                    self.dispatch(n.expr))
        return pyast.VarAssign(n.nodes[0].name, self.dispatch(n.expr))

    def visitIf(self, n):
        return pyast.If(map(lambda (x,y): (self.dispatch(x), self.dispatch(y)), 
                            n.tests),
                        self.dispatch(n.else_))
    
    def visitDiscard(self, n):
        return pyast.Discard(self.dispatch(n.expr))
    
    def visitFunction(self, n):
        return pyast.Function(n.name, n.argnames, self.dispatch(n.code))

    # Terminal Expressions

    def visitConst(self, n):
        return pyast.Const(n.value)

    def visitName(self, n):
        return pyast.Name(n.name)

    # Non-Terminal Expressions

    def visitGetattr(self, n):
        return pyast.GetAttr(self.dispatch(n.expr), n.attrname)

    def visitLambda(self, n):
        return pyast.Lambda(n.argnames, self.dispatch(n.code))

    def visitReturn(self, n):
        return pyast.Return(self.dispatch(n.value))

    def visitList(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return pyast.List(nodes)

    def visitDict(self, n):
        items = []
        for item in n.items:
            key = self.dispatch(item[0])
            value = self.dispatch(item[1])
            items += [(key, value)]
        return pyast.Dict(items)

    def visitSubscript(self, n):
        assert n.flags != 'OP_ASSIGN'
        expr = self.dispatch(n.expr)
        subs = []
        for sub in n.subs:
            subs += [self.dispatch(sub)]
        return pyast.Subscript(expr, subs)
    
    def visitCompare(self, n):
        ops = []
        for op in n.ops:
            newop = (op[0], self.dispatch(op[1]))
            ops += [newop]
        return pyast.Compare(self.dispatch(n.expr), ops)

    def visitAdd(self, n):
        return pyast.Add((self.dispatch(n.left), self.dispatch(n.right)))
    
    def visitOr(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return pyast.Or(nodes)

    def visitAnd(self, n):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return pyast.And(nodes)

    def visitNot(self, n):
        return pyast.Not(self.dispatch(n.expr))

    def visitUnarySub(self, n):
        return pyast.UnarySub(self.dispatch(n.expr))

    def visitIfExp(self, n):
        return pyast.IfExp(self.dispatch(n.test),
                           self.dispatch(n.then),
                           self.dispatch(n.else_))    
    
    def visitCallFunc(self, n):
        args = []
        for arg in n.args:
            args += [self.dispatch(arg)]
        return pyast.CallFunc(self.dispatch(n.node), args)

    def visitWhile(self, n):
        return pyast.While(self.dispatch(n.test),
                           self.dispatch(n.body),
                           self.dispatch(n.else_) if n.else_ else None)
