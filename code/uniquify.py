# CU CS5525
# Fall 2012
# Python Compiler
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
#    Andy Sayler
#       http://www.andysayler.com
#    Michael (Mike) Vitousek
#       http://csel.cs.colorado.edu/~mivi2269/

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
