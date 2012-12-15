# CU CS5525
# Fall 2012
# GSV Python Compiler
#
# instr_select.py
# Visitor Funcations for x86 Instruction Selection
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
from set_visitor import SetVisitor

# Helper Tools
from functionwrappers import RESERVED_NAMES

def name(n):
    if isinstance(n, Name):
        return n.name
    else: raise Exception('Getting name of invalid node ' + str(n))

class FreeVarsVisitor(SetVisitor):
    def __init__(self):
        super(FreeVarsVisitor,self).__init__()
        self.local_visitor = LocalVarsVisitor()

    def visitVarAssign(self, n):
        return self.dispatch(n.value) - set([n.target])

    def visitName(self, n):
        if n.name in RESERVED_NAMES:
            return set([])
        else: return set([name(n)])

    # Non-Terminal Expressions

    def visitLet(self, n):
        return self.dispatch(n.rhs) | (self.dispatch(n.body) - self.dispatch(n.var))

    def visitSLambda(self, n):
        n.free_vars = self.dispatch(n.code) - (set(n.params) | self.local_visitor.preorder(n.code)) 
        return n.free_vars

class LocalVarsVisitor(SetVisitor):
    def visitModule(self, n):
        n.local_vars = self.dispatch(n.node)
        return n.local_vars

    def visitSLambda(self, n):
        n.local_vars = self.dispatch(n.code) - set(n.params)
        return set([])

    def visitVarAssign(self, n):
        return set([n.target]) | self.dispatch(n.value)

class NestedFreeVarsVisitor(SetVisitor):
    def visitSLambda(self, n):
        return n.free_vars
