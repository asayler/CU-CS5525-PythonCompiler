# CU CS5525
# Fall 2012
# GSV Python Compiler
#
# declassify.py
# Visitor Functions to Declassify AST
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
from copy_visitor import CopyVisitor
from assignee_visitor import AssigneeVisitor

# Helper Types
from functionwrappers import *
from utilities import generate_name

# OFF DA HOOK #
def specializeCallFunc(self, n):
    if isinstance(n.node, Name) and n.node.name in RESERVED_NAMES:
        return CallFunc(self.dispatch(n.node), map(self.dispatch, n.args))
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
                                   Let(Name(discardtemp),
                                       CallFunc(CallGETFUNCTION([GetAttr(Name(ftemp), '__init__')]), 
                                                [Name(objtemp)]+vals),
                                       Name(objtemp)),
                                   Name(objtemp))),
                         IfExp(CallISBOUNDMETHOD([Name(ftemp)]),
                               CallFunc(CallGETFUNCTION([Name(ftemp)]), 
                                        [CallGETRECEIVER([Name(ftemp)])]+vals),
                               IfExp(CallISUNBOUNDMETHOD([Name(ftemp)]),
                                     CallFunc(CallGETFUNCTION([Name(ftemp)]), vals),
                                     CallFunc(Name(ftemp), vals))))
    return Let(Name(ftemp), self.dispatch(n.node), gen_arg(n.args, []))

class ClassFindVisitor(CopyVisitor):
    def __init__(self):
        super(ClassFindVisitor,self).__init__()
        self.assignee_visitor = AssigneeVisitor()

    def preorder(self, tree, outside_scope, *args):
        scope = self.assignee_visitor.preorder(tree) | outside_scope
        return super(ClassFindVisitor, self).preorder(tree, scope)

    def preorder_expr(self, tree, *args):
        return super(ClassFindVisitor, self).preorder(tree, *args)

    def visitModule(self, n, scope):
        return Module(self.dispatch(n.node, scope))

    def visitStmtList(self, n, scope):
        nodes = []
        for s in n.nodes:
            if isinstance(s, Class):
                nodes += self.dispatch(s, scope)
            else:
                nodes += [self.dispatch(s, scope)]
        return StmtList(nodes)

    def visitClass(self, n, scope):
        classtemp = generate_name(n.name + '_temp')
        bases = map(self.dispatch, n.bases)
        stmts = [VarAssign(classtemp, 
                           CallCREATECLASS([List(bases)]))]
        stmts += DeclassifyVisitor(classtemp, self).preorder(n.code, scope).nodes
        stmts += [VarAssign(n.name, Name(classtemp))]
        return stmts

    def visitFunction(self, n, scope):
        scope = scope | self.assignee_visitor.preorder(n.code)
        return Function(n.name, n.args, self.dispatch(n.code, scope))

    def visitCallFunc(self, n, *args):
        return specializeCallFunc(self,n) 
    
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

    def visitVarAssign(self, n):
        return AttrAssign(Name(self.name), n.target, 
                          self.dispatch(n.value))
    
    def visitName(self, n):
        if n.name in self.assignees:
            if n.name in self.outside_scope:
                return IfExp(CallHASATTR([Name(self.name), String(n.name)]),
                             GetAttr(Name(self.name), n.name),
                             Name(n.name))
            else:
                return GetAttr(Name(self.name), n.name)
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

    def visitStmtList(self, n):
        nodes = []
        for s in n.nodes:
            if isinstance(s, Class) or isinstance(s, Function):
                nodes += self.dispatch(s)
            else:
                nodes += [self.dispatch(s)]
        return StmtList(nodes)

    def visitCallFunc(self, n):
        return specializeCallFunc(self, n) 

