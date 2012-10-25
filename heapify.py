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

# Helper Types
from vis import Visitor

# Helper Tools
from utilities import generate_name
from unitcopy import CopyVisitor
from free_vars import *

from functionwrappers import *

# Data Types
from compiler.ast import *
from monoast import *

#Assumption: Let-bound variables cannot be free in nested functions

ZERO = InjectFrom(INT_t, Const(0))

class HeapifyVisitor(CopyVisitor):
    def __init__(self):
        super(HeapifyVisitor,self).__init__()
        del CopyVisitor.visitAdd
        del CopyVisitor.visitUnarySub
        del CopyVisitor.visitNot
        del CopyVisitor.visitCompare
        CopyVisitor.visitIsTag = IsTag.visitIsTag
        CopyVisitor.visitProjectTo = ProjectTo.visitProjectTo
        CopyVisitor.visitInjectFrom = InjectFrom.visitInjectFrom
        CopyVisitor.visitLet = Let.visitLet
        CopyVisitor.visitIntAdd = IntAdd.visitIntAdd
        CopyVisitor.visitIntEqual = IntEqual.visitIntEqual
        CopyVisitor.visitIntNotEqual = IntNotEqual.visitIntNotEqual
        CopyVisitor.visitIntUnarySub = IntUnarySub.visitIntUnarySub
        CopyVisitor.visitSubscriptAssign = SubscriptAssign.visitSubscriptAssign
        # Initialize helper visitors
        self.local_visitor = LocalVarsVisitor()
        self.free_visitor = FreeVarsVisitor()
        self.nested_visitor = NestedFreeVarsVisitor()
        # Global set of variables needing heapification
        self.needs_heapification = set([])
        
    def preorder(self, tree, *args):
        self.local_visitor.preorder(tree)
        self.free_visitor.preorder(tree)
        return super(HeapifyVisitor, self).preorder(tree, *args)

    def visitSLambda(self, n):
        lvs = n.local_vars
        self.needs_heapification = self.needs_heapification | self.nested_visitor.preorder(n.code)
        code = self.dispatch(n.code)
        new_params = []
        new_stmts = []
        for param in n.params:
            if param in self.needs_heapification:
                new_param = generate_name('heaped@')+param
                new_stmts.append(Assign([AssName(param, 'OP_ASSIGN')], List([ZERO])))
                new_stmts.append(SubscriptAssign(Name(param), ZERO, Name(new_param)))
                new_params.append(new_param)
            else:
                new_params.append(param)
        for local in lvs:
            if local in self.needs_heapification:
                new_stmts.append(Assign([AssName(local, 'OP_ASSIGN')], List([ZERO])))
        ret = SLambda(new_params, Stmt(new_stmts + code.nodes))
        ret.free_vars = n.free_vars
        return ret

    def visitAssign(self, n):
        if n.nodes[0].name in self.needs_heapification:
            return SubscriptAssign(Name(name), ZERO, self.dispatch(n.expr))
        else: return Assign(n.nodes, self.dispatch(n.expr)) 

    def visitName(self, n):
        if n.name in self.needs_heapification:
            return Subscript(Name(n.name), 'OP_APPLY', [ZERO])
        else: return n
