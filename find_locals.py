from compiler.ast import *
from set_visitor import SetVisitor

def name(n):
    if isinstance(n, Name) or isinstance(n, AssName):
        return n.name
    else: raise Exception('Getting name of invalid node ' + str(n))

class FindLocalsVisitor(SetVisitor):

    def visitClass(self, n):
        return set([n.name])

    def visitFunction(self, n):
        return set([n.name])

    def visitAssName(self, n):
        return set([name(n)])
