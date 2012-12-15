# CU CS5525
# Fall 2012
# GSV Python Compiler
#
# ssa.py
# Visitor Functions to convert AST to SSA
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

# Helper Tools
from utilities import generate_name, make_assign
from copy_visitor import CopyVisitor
from assignee_visitor import AssigneeVisitor

from functionwrappers import *

# Data Types
from pyast import *

class SSAVisitor(CopyVisitor):
    assign_find = AssigneeVisitor()

    def make_ssa_write(self, name, special=None):
        if name in RESERVED_NAMES:
            return name
        else: return "%s$%s" % (name, special if special else self.names[name])

    def make_ssa_read(self, name, special=None):
        if name in RESERVED_NAMES:
            return name
        else: return "%s$%s" % (name, special if special else self.scope[name])
        

    def preorder(self, tree):
        self.names = {}
        self.scope = {}
        return super(SSAVisitor, self).preorder(tree)

    def visitVarAssign(self, n):
        value = self.dispatch(n.value)
        if not n.target in RESERVED_NAMES:
            self.names[n.target] = (self.names[n.target] + 1) if \
                n.target in self.names else 0
            self.scope[n.target] = self.names[n.target]
        return VarAssign(self.make_ssa_write(n.target), value)

    def visitName(self, n):
        return Name(self.make_ssa_read(n.name))

    def visitSLambda(self, n):
        params = []
        for param in n.params:
            self.names[param] = (self.names[param] + 1) if \
                param in self.names else 0
            self.scope[param] = self.names[param]
            params.append(self.make_ssa_write(param))
        return SLambda(params, self.dispatch(n.code), n.label)

    def visitIf(self, n):
        assign_body1 = self.assign_find.preorder(n.tests[0][1])
        assign_else = self.assign_find.preorder(n.else_)
        pre_assigns = set([x for x in assign_body1 if x in self.names]) | \
            set([y for y in assign_else if y in self.names])
        common_assigns = assign_body1.intersection(assign_else)
        assigns = pre_assigns | common_assigns
        prephi = {}
        for x in pre_assigns:
            prephi[x] = self.make_ssa_read(x)
        tests = []
        bodies = []
        dicts = []
        choices = []
        for (test, _) in n.tests:
            tests.append(self.dispatch(test))
        topscope = self.scope.copy()
        for (_, body) in n.tests:
            bodies.append(self.dispatch(body))
            lchoices = {}
            for x in assigns:
                if x in assign_body1:
                    lchoices[x] = self.make_ssa_write(x)
                else: lchoices[x] = prephi[x]
            choices.append(lchoices)
            self.scope = topscope.copy()
        else_ = self.dispatch(n.else_)
        elsechoices = {}
        phimunge = {}
        phinames = []
        for x in assigns:
            if x in assign_else:
                elsechoices[x]=self.make_ssa_read(x)
            else: elsechoices[x]=append(prephi[x])

            self.names[x] = self.names[x] + 1
            self.scope[x] = self.names[x]
            phimunge[x] = self.make_ssa_write(x)
            phinames.append(phimunge[x])
        finalchoices = []
        finalelsechoices = {}
        for lchoices in choices:
            finallchoice = {}
            for x in lchoices:
                finallchoice[phimunge[x]] = lchoices[x]
            finalchoices.append(finallchoice)
        for x in elsechoices:
            finalelsechoices[phimunge[x]] = elsechoices[x]
        return IfPhi(zip(tests,bodies,finalchoices), (else_, finalelsechoices))

    def visitWhileFlat(self, n):
        assigns = [x for x in (self.assign_find.preorder(n.body))
                   if x in self.names]
        prephi = {}
        for x in assigns:
            prephi[x] = self.make_ssa_read(x)
        phicounts = {}
        for x in assigns:
            phicount = self.names[x] + 1
            self.names[x] = phicount
            self.scope[x] = phicount
            phicounts[x] = phicount
        phi = {}
        testss = self.dispatch(n.testss)
        test = self.dispatch(n.test)
        body = self.dispatch(n.body)    
        for x in assigns:
            xphi = [prephi[x], self.make_ssa_read(x)]
            phi[self.make_ssa_write(x, phicounts[x])] = xphi
            self.scope[x] = phicounts[x]
        return WhileFlatPhi(phi, 
                            testss, 
                            test, body, 
                            self.dispatch(n.else_) if n.else_ else None)
            
            
        
