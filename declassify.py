# CU CS5525
# Fall 2012
# Python Compiler
#
# explicate.py
# Visitor Functions to Explicate AST
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

import sys

# Data Types
from compiler.ast import *
from monoast import *
from set_visitor import *

from unitcopy import CopyVisitor

# Helper Types
from vis import Visitor
from functionwrappers import *
from utilities import generate_name

# OFF DA HOOK #
def specializeCallFunc(self, n):
    if isinstance(n.node, Name) and n.node.name in RESERVED_NAMES:
        return CallFunc(self.dispatch(n.node), map(self.dispatch, n.args),  n.star_args, n.dstar_args, n.lineno)
    ftemp = generate_name('func')
    def gen_arg(args, vals):
        if args:
            temp = generate_name('arg')
            return Let(Name(temp), self.dispatch(args[0]), gen_arg(args[1:], 
                                                                       vals + [Name(temp)]))
        else:
            objtemp = generate_name('obj')
            initemp = generate_name('ini')
            discardtemp = generate_name('discard')
            return IfExp(CallISCLASS([Name(ftemp)]),
                             Let(Name(objtemp), CallCREATEOBJECT([Name(ftemp)]),
                                 IfExp(CallHASATTR([Name(ftemp), String('__init__')]),
                                       Let(Name(discardtemp), CallFunc(CallGETFUNCTION([Getattr(Name(ftemp), '__init__')]), 
                                                                       [Name(objtemp)]+vals, n.star_args, n.dstar_args, n.lineno),
                                           Name(objtemp)),
                                       Name(objtemp))),
                         IfExp(CallISBOUNDMETHOD([Name(ftemp)]),
                                   CallFunc(CallGETFUNCTION([Name(ftemp)]), 
                                            [CallGETRECEIVER([Name(ftemp)])]+vals, n.star_args, n.dstar_args, n.lineno),
                               IfExp(CallISUNBOUNDMETHOD([Name(ftemp)]),
                                     CallFunc(CallGETFUNCTION([Name(ftemp)]), vals, n.star_args, n.dstar_args, n.lineno),
                                     CallFunc(Name(ftemp), vals, n.star_args, n.dstar_args, n.lineno))))
    return Let(Name(ftemp), self.dispatch(n.node), gen_arg(n.args, []))
    
class ClassFindVisitor(CopyVisitor):
    def __init__(self):
        super(ClassFindVisitor,self).__init__()
        del CopyVisitor.visitAssAttr
        CopyVisitor.visitSubscriptAssign = SubscriptAssign.visitSubscriptAssign
        CopyVisitor.visitAttrAssign = AttrAssign.visitAttrAssign
        self.assignee_visitor = AssigneeVisitor()

    def preorder(self, tree, outside_scope, *args):
        scope = self.assignee_visitor.preorder(tree) | outside_scope
        return super(ClassFindVisitor, self).preorder(tree, scope)

    def preorder_expr(self, *args):
        return super(ClassFindVisitor, self).preorder(tree, *args)

    def visitModule(self, n, scope):
        return Module(n.doc, self.dispatch(n.node, scope), n.lineno)

    def visitStmt(self, n, scope):
        nodes = []
        for s in n.nodes:
            if isinstance(s, Class):
                nodes += self.dispatch(s, scope)
            else:
                nodes += [self.dispatch(s, scope)]
        return Stmt(nodes, n.lineno)

    def visitClass(self, n, scope):
        classtemp = generate_name(n.name + '_temp')
        bases = map(self.dispatch, n.bases)
        stmts = [Assign([AssName(classtemp, 'OP_ASSIGN')], 
                        CallCREATECLASS([List(bases)]))]
        stmts += DeclassifyVisitor(classtemp, self).preorder(n.code, scope)
        stmts += [Assign([AssName(n.name, 'OP_ASSIGN')], Name(classtemp))]
        return stmts

    def visitFunction(self, n, scope):
        print scope, type(scope)
        scope = scope | self.assignee_visitor.preorder(n.code)
        return Function(n.decorators, n.name, n.argnames, n.defaults,
                        n.flags, n.doc, self.dispatch(n.code, scope))

    def visitCallFunc(self, n):
        return specializeCallFunc(self,n) 

    def visitIf(self, n, scope):
        return If(map(lambda (x,y): (self.dispatch(x), 
                                     self.dispatch(y, scope)), 
                      n.tests),
                  self.dispatch(n.else_, scope))

    def visitDiscard(self, n, scope):
        return Discard(self.dispatch(n.expr), n.lineno)

    def visitPrintnl(self, n, scope):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return Printnl(nodes, n.dest, n.lineno)

    def visitSubscriptAssign(self, n, scope):
        return SubscriptAssign(self.dispatch(n.target), self.dispatch(n.sub), self.dispatch(n.value))

    def visitAttrAssign(self, n, scope):
        return AttrAssign(self.dispatch(n.target), n.attr, self.dispatch(n.value))

    def visitAssign(self, n, scope):
        nodes = []
        for node in n.nodes:
            nodes += [self.dispatch(node)]
        return Assign(nodes, self.dispatch(n.expr), n.lineno)

    def visitReturn(self, n, scope):
        return Return(self.dispatch(n.value))

    def visitIf(self, n, scope):
        return If(map(lambda (x,y): (self.dispatch(x), self.dispatch(y, scope)), 
                      n.tests),
                  self.dispatch(n.else_, scope))

    def visitWhile(self, n, scope):
        return While(self.dispatch(n.test),
                     self.dispatch(n.body, scope),
                     self.dispatch(n.else_, scope) if n.else_ else None,
                     n.lineno)

    
class DeclassifyVisitor(CopyVisitor):
    def __init__(self, name, finder):
        super(DeclassifyVisitor,self).__init__()
        self.name = name
        self.assignee_visitor = AssigneeVisitor()
        self.finder = finder

    def preorder(self, tree, outside_scope, *args):
        self.assignees = self.assignee_visitor.preorder(tree)
        self.outside_scope = outside_scope
        return super(DeclassifyVisitor, self).preorder(tree, *args)

    def visitAssign(self, n):
        return AttrAssign(Name(self.name), n.nodes[0].name, 
                          self.dispatch(n.expr))
        
    def visitName(self, n):
        if n.name in self.assignees:
            if n.name in self.outside_scope:
                return IfExp(CallHASATTR([Name(self.name), String(n.name)]),
                             Getattr(Name(self.name), n.name),
                             Name(n.name))
            else:
                return Getattr(Name(self.name), n.name)
        else:
            return Name(n.name)

    def visitFunction(self, n):
        temp = generate_name(n.name + '_temp')
        name = n.name
        n.name = temp
        n = self.finder.preorder(n, self.outside_scope)
        return [n, AttrAssign(Name(self.name), name, Name(temp))]

    def visitClass(self, n):
        temp = generate_name(n.name + '_temp')
        name = n.name
        n.name = temp
        n = self.finder.preorder(n, self.outside_scope)
        return n + [AttrAssign(Name(self.name), name, Name(temp))]

    def visitLambda(self, n):
        return self.finder.preorder_expr(n)

    def visitStmt(self, n):
        nodes = []
        for s in n.nodes:
            if isinstance(s, Class) or isinstance(s, Function):
                nodes += self.dispatch(s)
            else:
                nodes += [self.dispatch(s)]
        return Stmt(nodes, n.lineno)

    def visitCallFunc(self, n):
        return specializeCallFunc(self, n) 

class AssigneeVisitor(SetVisitor):
    def visitAssName(self, n):
        return set([n.name])
        
    def visitFunction(self, n):
        return set([n.name])

    def visitClass(self, n):
        return set([n.name])
