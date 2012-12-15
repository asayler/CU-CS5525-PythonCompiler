# CU CS5525
# Fall 2012
# GSV Python Compiler
#
# uniquify.py
# Visitor Funstions to Uniquify AST
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

# System Types
import copy

# Data Types
from pyast import *

# Parents
from copy_visitor import CopyVisitor

# Helper Types
from find_locals import FindLocalsVisitor
from utilities import generate_name 

class UniquifyVisitor(CopyVisitor):

    def __init__(self):
        super(UniquifyVisitor, self).__init__()

    # Modules
    def visitModule(self, n):
        local_vars = FindLocalsVisitor().preorder(n.node)
        renaming = {}
        for v in local_vars:
            renaming[v] = generate_name(v)
        return Module(self.dispatch(n.node, renaming))

    def visitVarAssign(self, n, renaming):
        rhs = self.dispatch(n.value, renaming)
        lhs = renaming[n.target]
        return VarAssign(lhs, rhs)

    def visitName(self, n, renaming):
        if n.name in renaming.keys():
            return Name(renaming[n.name])
        else:
            return n

    def visitFunction(self, n, renaming):
        new_renaming = copy.deepcopy(renaming)
        local_vars = FindLocalsVisitor().preorder(n.code) | set(n.args)
        for v in local_vars:
            new_renaming[v] = generate_name(v)
        return Function(renaming[n.name],
                        [new_renaming[x] for x in n.args],
                        self.dispatch(n.code, new_renaming))

    def visitLambda(self, n, renaming):
        new_renaming = copy.deepcopy(renaming)
        local_vars = n.args
        for v in local_vars:
            new_renaming[v] = generate_name(v)        
        return Lambda([new_renaming[x] for x in n.args],
                      self.dispatch(n.expr, new_renaming))

    def visitLet(self, n, renaming):
        new_renaming = copy.deepcopy(renaming)
        new_renaming[n.var] = generate_name(n.var.name)
        var  = self.dispatch(n.var, new_renaming)
        rhs  = self.dispatch(n.rhs, renaming)
        body = self.dispatch(n.body, new_renaming)
        return Let(var, rhs, body)
