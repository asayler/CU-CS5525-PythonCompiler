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
from utilities import make_assign
from unitcopy import CopyVisitor

from functionwrappers import *

# Data Types
from compiler.ast import *
from monoast import *

MAINNAME = 'main'

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
            stmts += [Return(Const(0))]
            slambdas += [SLambda([], Stmt(stmts), MAINNAME)]
            return slambdas
        else:
            return (Stmt(stmts), slambdas)

    def visitAssign(self, n):
        (expr, slambdas) = self.dispatch(n.expr)
        return (Assign(n.nodes, expr), slambdas)
    
    def visitDiscard(self, n):
        (expr, slambdas) = self.dispatch(n.expr)
        return (Discard(expr), slambdas)

    def visitIf(self, n):
        slambdas = []
        tests = []
        for (test, body) in n.tests:
            (test, rslambdas) = self.dispatch(test)
            slambdas += rslambdas
            (then, rslambdas) = self.dispatch(body, False)
            slambdas += rslambdas
            tests.append((test, then))
        (else_, rslambdas) = self.dispatch(n.else_, False)
        slambdas += rslambdas
        return (If(tests, else_), slambdas)

    def visitReturn(self, n):
        (value, slambdas) = self.dispatch(n.value)
        return (Return(value), slambdas)

    def visitPrintnl(self, n):
        nodes = []
        slambdas = []
        for node in n.nodes:
            (node, slambda) = self.dispatch(node)
            nodes.append(node)
            slambdas += slambda
        return (Printnl(nodes, n.dest, n.lineno), slambdas)
    
    # Terminal Expressions

    def visitConst(self, n):
        return (Const(n.value), [])

    def visitName(self, n):
        return (Name(n.name), [])

    def visitString(self, n):
        return (n, [])

    # Non-Terminal Expressions - Convert

    def visitSLambda(self, n):
        # Creat New Label
        label_name = 'Q' + generate_name("SLambda")
        label = SLambdaLabel(label_name)
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
            fvs += [Name(var)]
            stmt = make_assign(var, Subscript(Name(fvs_n), 'OP_APPLY',
                                              [InjectFrom(INT_t, Const(cnt))]))
            stmts += [stmt]
            cnt += 1
        # Setup list of stmts
        stmts += code.nodes
        # Setup params, appending fvs
        params = []
        params += [fvs_n]
        params += n.params
        # Create new closed slambda
        slambdas += [SLambda(params, Stmt(stmts), label_name)]
        # Return Call and list of SLambdas
        return (InjectFrom(BIG_t, CallCREATECLOSURE([label, List(fvs)])), slambdas)

    def visitIndirectCallFunc(self, n):
        slambdas = []
        (node, rslambdas) = self.dispatch(n.node)
        slambdas += rslambdas
        args = []
        for arg in n.args:
            (rarg, rslambdas) = self.dispatch(arg)
            args += [rarg]
            slambdas += rslambdas
        tmpname = generate_name('let_ICF')
        tmpvar = Name(tmpname)
        t = Let(tmpvar, node, IndirectCallFunc(CallGETFUNPTR([tmpvar]),
                                               ([CallGETFREEVARS([tmpvar])] + args)))
        return (t, slambdas)

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
            args += [rarg]
            slambdas += rslambdas
        (node, rslambdas) = self.dispatch(n.node)
        slambdas += rslambdas
        return (CallFunc(node, args), slambdas)

    def visitIfExp(self, n):
        slambdas = []
        (test, rslambdas) = self.dispatch(n.test)
        slambdas += rslambdas
        (then, rslambdas) = self.dispatch(n.then)
        slambdas += rslambdas
        (else_, rslambdas) = self.dispatch(n.else_)
        slambdas += rslambdas
        return (IfExp(test, then, else_), slambdas)

    def visitInjectFrom(self, n):
        (arg, slambdas) = self.dispatch(n.arg)
        return (InjectFrom(n.typ, arg), slambdas)

    def visitProjectTo(self, n):
        (arg, slambdas) = self.dispatch(n.arg)
        return (ProjectTo(n.typ, arg), slambdas)

    def visitIsTag(self, n):
        (arg, slambdas) = self.dispatch(n.arg)
        return (IsTag(n.typ, arg), slambdas)

    def visitIntAdd(self, n):
        slambdas = []
        (left, rslambdas) = self.dispatch(n.left)
        slambdas += rslambdas
        (right, rslambdas) = self.dispatch(n.right)
        slambdas += rslambdas
        return (IntAdd((left, right)), slambdas)

    def visitIntUnarySub(self, n):
        (expr, slambdas) = self.dispatch(n.expr)
        return (IntUnarySub(expr), slambdas)

    def visitIntEqual(self, n):
        slambdas = []
        (left, rslambdas) = self.dispatch(n.left)
        slambdas += rslambdas
        (right, rslambdas) = self.dispatch(n.right)
        slambdas += rslambdas 
        return (IntEqual((left, right)), slambdas)

    def visitIntNotEqual(self, n):
        slambdas = []
        (left, rslambdas) = self.dispatch(n.left)
        slambdas += rslambdas
        (right, rslambdas) = self.dispatch(n.right)
        slambdas += rslambdas 
        return (IntNotEqual((left, right)), slambdas)

    def visitSubscriptAssign(self, n):
        slambdas = []
        (target, rslambdas) = self.dispatch(n.target)
        slambdas += rslambdas
        (sub, rslambdas) = self.dispatch(n.sub)
        slambdas += rslambdas
        (value, rslambdas) = self.dispatch(n.value)
        slambdas += rslambdas
        return (SubscriptAssign(target, sub, value), slambdas)

    def visitSubscript(self, n):
        slambdas = []
        (expr, rslambdas) = self.dispatch(n.expr)
        slambdas += rslambdas
        subs = []
        for sub in n.subs:
            (rsub, rslambdas) = self.dispatch(sub)
            subs += [rsub]
            slambdas += rslambdas
        return (Subscript(expr, n.flags, subs), slambdas)

    def visitAnd(self, n):
        slambdas = []
        nodes = []
        for node in n.nodes:
            (rnode, rslambdas) = self.dispatch(node)
            nodes += [rnode]
            slambdas += rslambdas
        return (And(nodes), slambdas)
        
    def visitOr(self, n):
        slambdas = []
        nodes = []
        for node in n.nodes:
            (rnode, rslambdas) = self.dispatch(node)
            nodes += [rnode]
            slambdas += rslambdas
        return (Or(nodes), slambdas)

    def visitLet(self, n):
        slambdas = []
        (var, rslambdas) = self.dispatch(n.var)
        slambdas += rslambdas
        (rhs, rslambdas) = self.dispatch(n.rhs)
        slambdas += rslambdas
        (body, rslambdas) = self.dispatch(n.body)
        slambdas += rslambdas 
        return (Let(var, rhs, body), slambdas)

    def visitWhile(self, n):
        slambdas = []
        (test, rslambdas) = self.dispatch(n.test)
        slambdas += rslambdas
        (body, rslambdas) = self.dispatch(n.body, False)
        slambdas += rslambdas
        return (While(test, body, n.else_), slambdas)

