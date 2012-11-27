# CU CS5525
# Fall 2012
# Python Compiler
#
# heapify.py
# Visitor Funstions to Heapify AST
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
from utilities import generate_name
from copy_visitor import CopyVisitor
from free_vars import *
from functionwrappers import *

# Data Types
from pyast import *

ZERO = InjectFrom(INT_t, Const(0))

#Assumption: Let-bound variables cannot be free in nested functions

class HeapifyVisitor(CopyVisitor):
    def __init__(self):
        super(HeapifyVisitor,self).__init__()
        # Initialize helper visitors
        self.local_visitor = LocalVarsVisitor()
        self.free_visitor = FreeVarsVisitor()
        self.nested_visitor = NestedFreeVarsVisitor()
        
    def preorder(self, tree, *args):
        self.local_visitor.preorder(tree)
        self.free_visitor.preorder(tree)
        # Global set of variables needing heapification
        self.needs_heapification = set([])
        return super(HeapifyVisitor, self).preorder(tree, *args)

    def visitModule(self, n):
        self.needs_heapification = self.needs_heapification | self.nested_visitor.preorder(n.node)
        lvs = n.local_vars
        new_stmts = []
        for local in lvs:
            if local in self.needs_heapification:
                new_stmts.append(VarAssign(local, List([ZERO])))
        body = self.dispatch(n.node)
        body.nodes = new_stmts + body.nodes
        return Module(body)

    def visitSLambda(self, n):
        lvs = n.local_vars
        self.needs_heapification = self.needs_heapification | self.nested_visitor.preorder(n.code)
        code = self.dispatch(n.code)
        new_params = []
        new_stmts = []
        for param in n.params:
            if param in self.needs_heapification:
                new_param = generate_name('heaped@')+param
                new_stmts.append(VarAssign(param, List([ZERO])))
                new_stmts.append(SubscriptAssign(Name(param), [ZERO], Name(new_param)))
                new_params.append(new_param)
            else:
                new_params.append(param)
        for local in lvs:
            if local in self.needs_heapification:
                new_stmts.append(VarAssign(local, List([ZERO])))
        ret = SLambda(new_params, StmtList(new_stmts + code.nodes))
        ret.free_vars = n.free_vars
        return ret

    def visitVarAssign(self, n):
        if n.target in self.needs_heapification:
            return SubscriptAssign(Name(n.target), [ZERO], self.dispatch(n.value))
        else: return VarAssign(n.target, self.dispatch(n.value)) 

    def visitName(self, n):
        if n.name in self.needs_heapification:
            return Subscript(Name(n.name), [ZERO])
        else: return n
