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

# Data Types
from pyast import *

# Parents
from list_visitor import ListVisitor

# Helper Tools
from utilities import generate_name
from utilities import make_assign
from functionwrappers import *

MAINNAME = 'main'

class ClosureVisitor(ListVisitor):
    def __init__(self):
        super(ClosureVisitor,self).__init__()

    # Module

    def visitModule(self, n):
        return Program(self.dispatch(n.node, True))

    # Staments

    def visitStmtList(self, n, is_main):
        slambdas = []
        stmts = []
        for node in n.nodes:
            (rstmt, rslambdas) = self.dispatch(node)
            stmts += [rstmt]
            slambdas += rslambdas
        if(is_main):
            stmts += [Return(Const(0))]
            slambdas += [SLambda([], StmtList(stmts), MAINNAME)]
            return slambdas
        else:
            return (StmtList(stmts), slambdas)

    def visitVarAssign(self, n):
        (expr, slambdas) = self.dispatch(n.value)
        return (VarAssign(n.target, expr), slambdas)

    def visitAttrAssign(self, n):
        (target, tlambdas) = self.dispatch(n.target)
        (value, vlambdas) = self.dispatch(n.value)
        return (AttrAssign(target, n.attr, value), tlambdas + vlambdas)

    def visitSubscriptAssign(self, n):
        (target, tlambdas) = self.dispatch(n.target)
        plist = map(self.dispatch, n.subs)
        slambdas = []
        subs = []
        for (sub, lambdas) in plist:
            slambdas += lambdas
            subs += [sub]
        (value, vlambdas) = self.dispatch(n.value)
        return (SubscriptAssign(target, subs, value), tlambdas + slambdas + vlambdas)
    
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

    def visitWhile(self, n):
        slambdas = []
        (test, rslambdas) = self.dispatch(n.test)
        slambdas += rslambdas
        (body, rslambdas) = self.dispatch(n.body, False)
        slambdas += rslambdas
        return (While(test, body, n.else_), slambdas)

    # Non-Terminal Expressions - Convert

    def visitSLambda(self, n):
        # Creat New Label
        label_name = 'Q' + generate_name("SLambda")
        
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
            stmt = make_assign(var, Subscript(Name(fvs_n),
                                              [InjectFrom(INT_t, Const(cnt))]))
            stmts += [stmt]
            cnt += 1
        # Setup list of stmts
        stmts += code.nodes
        # Setup params, appending fvs
        params = []
        params += [fvs_n]
        params += n.params
        #Create SLambdaLabel
        label = SLambdaLabel(label_name, len(params))
        # Create new closed slambda
        slambdas += [SLambda(params, StmtList(stmts), label_name)]
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

    def visitIfExp(self, n):
        test, sl1 = self.dispatch(n.test)
        then, sl2 = self.dispatch(n.then)
        else_, sl3 = self.dispatch(n.else_)
        return (IfExp(test, then, else_), sl1 + sl2 + sl3)
