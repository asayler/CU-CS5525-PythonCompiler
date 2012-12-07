# CU CS5525
# Fall 2012
# Python Compiler
#
# py3parse.py
# Prase Infrastructure using new Python AST built-in parser
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

from ast import *
from ast import parse as astparse
import pyast
from vis import *

def parse(inputFilePath):
    f = open(inputFilePath, 'r')
    filedata = f.read()
    f.close()
    parsedast = astparse(filedata)
    return ParseConvert().preorder(parsedast)

class ParseConvert(Visitor):
    def visitModule(self, n):
        return pyast.Module(pyast.StmtList(map(self.dispatch, n.body)))
    
    def visitClassDef(self, n):
        return pyast.Class(n.name, map(self.dispatch, n.bases), 
                           pyast.StmtList(map(self.dispatch, n.body)))

    def visitPrint(self, n):
        nodes = []
        for node in n.values:
            nodes += [self.dispatch(node)]
        return pyast.Discard(pyast.CallFunc(pyast.Name('print_any'), nodes))

    def visitAssign(self, n):
        if isinstance(n.targets[0], Subscript):
            subs = []
            target = n.targets[0]
            while isinstance(target, Subscript):
                subs += [target.slice.value]
                target = target.value
            subs.reverse()
            return pyast.SubscriptAssign(self.dispatch(target), 
                                         map(self.dispatch, subs),
                                         self.dispatch(n.value))
        elif isinstance(n.targets[0], Attribute):
            return pyast.AttrAssign(self.dispatch(n.targets[0].value), 
                                    n.targets[0].attr,
                                    self.dispatch(n.value))
        return pyast.VarAssign(n.targets[0].id, self.dispatch(n.value))

    def visitIf(self, n):
        return pyast.If([(self.dispatch(n.test),
                          pyast.StmtList(map(self.dispatch, n.body)))],
                        pyast.StmtList(map(self.dispatch, n.orelse)))
    
    def visitExpr(self, n):
        return pyast.Discard(self.dispatch(n.value))
    
    def visitFunctionDef(self, n):
        return pyast.Function(n.name, map(lambda x: x.id, n.args.args), 
                              pyast.StmtList(map(self.dispatch, n.body)))

    # Terminal Expressions

    def visitNum(self, n):
        return pyast.Const(n.n)

    def visitName(self, n):
        return pyast.Name(n.id)

    # Non-Terminal Expressions

    def visitAttribute(self, n):
        return pyast.GetAttr(self.dispatch(n.value), n.attr)

    def visitLambda(self, n):
        return pyast.Lambda(map(lambda x: x.id, n.args.args), 
                            self.dispatch(n.body))

    def visitReturn(self, n):
        return pyast.Return(self.dispatch(n.value))

    def visitList(self, n):
        nodes = []
        for node in n.elts:
            nodes += [self.dispatch(node)]
        return pyast.List(nodes)

    def visitDict(self, n):
        items = []
        for item in zip(n.keys,n.values):
            key = self.dispatch(item[0])
            value = self.dispatch(item[1])
            items += [(key, value)]
        return pyast.Dict(items)

    def visitSubscript(self, n):
        subs = []
        target = n
        while isinstance(target, Subscript):
            subs += [self.dispatch(target.slice.value)]
            target = target.value
        subs.reverse()
        return pyast.Subscript(self.dispatch(target), subs)
    
    def visitCompare(self, n):
        ops = []
        for op in zip(n.ops, n.comparators):
            newop = (self.dispatch(op[0]), self.dispatch(op[1]))
            ops += [newop]
        return pyast.Compare(self.dispatch(n.left), ops)

    def visitEq(self, n):
        return '=='
    def visitIs(self, n):
        return 'is'
    def visitNotEq(self, n):
        return '!='
    def visitGt(self, n):
        return '>'
    def visitLt(self, n):
        return '<'

    def visitBinOp(self, n):
        return self.dispatch(n.op)((self.dispatch(n.left), 
                                    self.dispatch(n.right)))
    def visitAdd(self, n):
        return pyast.Add
    
    def visitBoolOp(self, n):
        nodes = []
        for node in n.values:
            nodes += [self.dispatch(node)]
        return self.dispatch(n.op)(nodes)
    def visitOr(self, n):
        return pyast.Or
    def visitAnd(self, n):
        return pyast.And

    def visitUnaryOp(self, n):
        return self.dispatch(n.op)(self.dispatch(n.operand))
    def visitNot(self, n):
        return pyast.Not
    def visitUSub(self, n):
        return pyast.UnarySub

    def visitIfExp(self, n):
        return pyast.IfExp(self.dispatch(n.test),
                           self.dispatch(n.body),
                           self.dispatch(n.orelse))    
    
    def visitCall(self, n):
        args = []
        for arg in n.args:
            args += [self.dispatch(arg)]
        return pyast.CallFunc(self.dispatch(n.func), args)

    def visitWhile(self, n):
        return pyast.While(self.dispatch(n.test),
                           pyast.StmtList(map(self.dispatch, n.body)),
                           pyast.StmtList(map(self.dispatch, n.orelse)) \
                               if n.orelse else None)
