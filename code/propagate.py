# CU CS5525
# Fall 2012
# Python Compiler
#
# propagate.py
# Visitor Functions to Remove Direct Assignments from AST
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

from functionwrappers import *

# Data Types
from pyast import *

class PropagateVisitor(CopyVisitor):
    
    def __init__(self):
        self.names = {}
        super(PropagateVisitor,self).__init__()

    def visitStmtList(self, n):
        stmts = []
        for node in n.nodes:
            stmt = self.dispatch(node)
            if(stmt != None):
                stmts += [stmt]
        return StmtList(stmts)

    def visitVarAssign(self, n):
        if(isinstance(n.value, Name)):
            if(n.value.name in self.names):
                n.value.name = self.names[n.value.name]
            if(n.target in self.names):
                raise Exception("SSA Violation")
            self.names[n.target] = n.value.name
            return None
        else:
            return VarAssign(n.target, self.dispatch(n.value))

    def visitName(self, n):
        if(n.name in self.names):
            name = self.names[n.name]
        else:
            name = n.name
        return Name(name)

    def visitWhileFlatPhi(self, n):
        new_phi = {}
        body = self.dispatch(n.body)
        for key in n.phi:
            values = n.phi[key]
            new_values = []
            for name in values:
                if name in self.names:
                    new_values.append(self.names[name])
                else: new_values.append(name)
            new_phi[key] = new_values
        return WhileFlatPhi(new_phi,
                            self.dispatch(n.testss),
                            self.dispatch(n.test),
                            body,
                            self.dispatch(n.else_) if n.else_ else None)

    # TODO: Handle Branching/Phi Update