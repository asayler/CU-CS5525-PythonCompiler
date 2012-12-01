from pyast import *
from set_visitor import SetVisitor

class AssigneeVisitor(SetVisitor):
    def visitVarAssign(self, n):
        return set([n.target])
    
    def visitFunction(self, n):
        return set([n.name])

    def visitClass(self, n):
        return set([n.name])
