# CU CS5525
# Fall 2012
# Python Compiler
#
# closureconvert.py
# Visitor Funstions to Closure Convert AST
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

from functionwrappers import *

# Data Types
from compiler.ast import *
from monoast import *

MAINNAME = '0_mainfunc'

class ClosureVisitor(CopyVisitor):
    def __init__(self):
        super(ClosureVisitor,self).__init__()
        CopyVisitor.visitSLambda = SLambda.visitSLambda

    # Module

    def visitModule(self, n):
        return Module(n.doc, self.dispatch(n.node, True))

    # Staments

    def visitStmt(self, n, is_main):
        slambdas = []
        stmts = []
        for node in n.nodes:
            (rstmt, rslambdas) = self.dispatch(node)
            stmts += [rstmt]
            slambdas += rslambdas
        if(is_main):
            slambdas += [SLambda([], stmts, SLambdaLabel(MAINNAME))]
            return slambdas
        else:
            return (Stmt(stmts), slambdas)

    def visitAssign(self, n):
        (expr, slambdas) = self.dispatch(n.expr)
        return (Assign(n.nodes, expr), slambdas)
    
    def visitDiscard(self, n):
        (expr, slambdas) = self.dispatch(n.expr)
        return (Discard(expr), slambdas)

    def visitReturn(self, n):
        (value, slambdas) = self.dispatch(n.value)
        return (Return(value), slambdas)
    
    # Terminal Expressions

    def visitConst(self, n):
        return (Const(n.value), [])

    def visitName(self, n):
        return (Name(n.name), [])

    # Non-Terminal Expressions - Convert

    def visitSLambda(self, n):
        # Creat New Label
        label = SLambdaLabel(generate_name("SLambda"))
        # Recurse on code body
        slambdas = []
        (code, rslambdas) = self.dispatch(n.code, False)
        slambdas += rslambdas
        # Setup fvs list
        fvs_n = generate_name("fvs")
        fvs = []
        # Setup each free variable
        stmts = []
        cnt = 0
        for var in n.free_vars:
            fvs += [var]
            stmt = make_assign(var, Subscript(Name(fvs_n), 'OP_APPLY',
                                              InjectFrom(INT_t, Const(cnt))))
            stmts += stmt
            cnt += 1
        # Setup list of stmts
        stmts += code.nodes
        # Setup params, appending fvs
        params = []
        params += [fvs_n]
        params += n.params
        # Create new closed slambda
        slambdas += [SLambda(params, Stmt(stmts), label)]
        # Return Call and list of SLambdas
        return (CallCREATECLOSURE([label, fvs]), slambdas)

    def visitIndirectCallFunc(self, n):
        return (n, [])

    # Non-Terminal Expressions - Copy

    def visitList(self, n):
        nodes = []
        slambdas = []
        for node in n.nodes:
            (rnode, rslambdas) = self.dispatch(node)
            nodes += [rnode]
            slambdas += rslambdas
        return (List(nodes), slambdas)

    def visitDict(self, n):
        items = []
        slambdas = []
        for item in n.items:
            (key, rslambdas) = self.dispatch(item[0])
            slambdas += rslambdas
            (value, rslambdas) = self.dispatch(item[1])
            slambdas += rslambdas
            items += [(key, value)]
        return (Dict(items), slambdas)

    def visitCallFunc(self, n):
        args = []
        slambdas = []
        for arg in n.args:
            (rarg, rslambdas) = self.dispatch(arg)
            args =+ [rarg]
            slambdas += rslambdas
        (node, rslambdas) = self.dispatch(n.node)
        slambdas += rslambdas
        return (CallFunc(node, args), slambdas)
