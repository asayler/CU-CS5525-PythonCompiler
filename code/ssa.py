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

# Helper Tools
from utilities import generate_name, make_assign
from copy_visitor import CopyVisitor
from assignee_visitor import AssigneeVisitor

from functionwrappers import *

# Data Types
from pyast import *

class SSAVisitor(CopyVisitor):
    assign_find = AssigneeVisitor()

    def make_ssa(self, name):
        if name in RESERVED_NAMES:
            return name
        else: return "%s$%s" % (name, self.names[name])

    def preorder(self, tree):
        self.names = {}
        return super(SSAVisitor, self).preorder(tree)

    def visitVarAssign(self, n):
        value = self.dispatch(n.value)
        if not n.target in RESERVED_NAMES:
            self.names[n.target] = (self.names[n.target] + 1) if \
                n.target in self.names else 0
        return VarAssign(self.make_ssa(n.target), value)

    def visitName(self, n):
        return Name(self.make_ssa(n.name))

    def visitSLambda(self, n):
        params = []
        for param in n.params:
            self.names[param] = (self.names[param] + 1) if \
                param in self.names else 0
            params.append(self.make_ssa(param))
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
            prephi[x] = self.make_ssa(x)
        tests = []
        bodies = []
        choices = []
        for (test, _) in n.tests:
            tests.append(self.dispatch(test))
        for (_, body) in n.tests:
            bodies.append(self.dispatch(body))
            lchoices = {}
            for x in assigns:
                if x in assign_body1:
                    lchoices[x] = self.make_ssa(x)
                else: lchoices[x] = prephi[x]
            choices.append(lchoices)
        else_ = self.dispatch(n.else_)
        phi = {}
        for x in assigns:
            xphi = []
            for lchoices in choices:
                xphi.append(lchoices[x])
            if x in assign_else:
                xphi.append(self.make_ssa(x))
            else: xphi.append(prephi[x])
            self.names[x] = self.names[x] + 1
            phi[self.make_ssa(x)] = xphi
        return IfPhi(zip(tests,bodies), else_, phi)

    def visitWhileFlat(self, n):
        assigns = [x for x in (self.assign_find.preorder(n.body))
                   if x in self.names]
        prephi = {}
        for x in assigns:
            prephi[x] = self.make_ssa(x)
        body = self.dispatch(n.body)
        phi = {}
        for x in assigns:
            xphi = [prephi[x], self.make_ssa(x)]
            self.names[x] = self.names[x] + 1
            phi[self.make_ssa(x)] = xphi
        return WhileFlatPhi(phi, 
                            self.dispatch(n.testss), 
                            self.dispatch(n.test), body, 
                            self.dispatch(n.else_) if n.else_ else None)
            
            
        
