# CU CS5525
# Fall 2012
# Python Compiler
#
# explicate.py
# Visitor Functions to Explicate AST
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

import sys

# Data Types
from compiler.ast import *
from monoast import *

from unitcopy import CopyVisitor

# Helper Types
from vis import Visitor
from functionwrappers import *
from utilities import generate_name

#Reserved Names
TRUENAME   = "True"
TRUEVALUE  = 1
FALSENAME  = "False"
FALSEVALUE = 0
TRUENODE   = InjectFrom(BOOL_t, Const(TRUEVALUE))
FALSENODE  = InjectFrom(BOOL_t, Const(FALSEVALUE))

COMPEQUAL    = '=='
COMPNOTEQUAL = '!='
COMPIS       = 'is'

class ExplicateVisitor(CopyVisitor):
    def __init__(self):
        super(ExplicateVisitor,self).__init__()
        CopyVisitor.visitLet = Let.visitLet
        
    # Helper Functions

    def projectType(self, expr):
        return IfExp(IsTag(BOOL_t, expr),
                     ProjectTo(BOOL_t, expr),
                     IfExp(IsTag(INT_t, expr),
                           ProjectTo(INT_t, expr),
                           ProjectTo(BIG_t, expr)))
    
    def explicateBinary(self, lhsexpr, rhsexpr, smallFunc, smallType, bigFunc, bigType, mixedDefault):
        lhsname = generate_name('let_binexp_lhs')
        rhsname = generate_name('let_binexp_rhs')
        lhsvar = Name(lhsname)
        rhsvar = Name(rhsname)
        t = Let(lhsvar,
                self.dispatch(lhsexpr),
                Let(rhsvar,
                    self.dispatch(rhsexpr),
                    # Small-Small Case
                    IfExp(And([Or([IsTag(BOOL_t, lhsvar),
                                   IsTag(INT_t, lhsvar)]),
                               Or([IsTag(BOOL_t, rhsvar),
                                   IsTag(INT_t, rhsvar)])]),
                          InjectFrom(smallType,
                                     smallFunc((self.projectType(lhsvar),
                                                self.projectType(rhsvar)))),
                          # Big-Big Case
                          IfExp(And([IsTag(BIG_t, lhsvar),
                                     IsTag(BIG_t, rhsvar)]),
                                InjectFrom(bigType,
                                           bigFunc([self.projectType(lhsvar),
                                                    self.projectType(rhsvar)])),
                                # Mixed Case
                                mixedDefault))))
        return t



    # Terminal Expressions

    def visitConst(self, n):
        # ToDo: Create IntConst type for use after explicate
        return InjectFrom(INT_t, Const(n.value, n.lineno))

    def visitName(self, n):
        if(n.name == TRUENAME):
            return TRUENODE
        elif(n.name == FALSENAME):
            return FALSENODE
        else:
            return Name(n.name, n.lineno)

    # Non-Terminal Expressions
        
    def visitCompare(self, n):
        # Process Single Pair
        lhsexpr = n.expr
        op      = n.ops[0][0]
        rhsexpr = n.ops[0][1]
        # Equal Compare
        if(op == COMPEQUAL):
            t = self.explicateBinary(lhsexpr, rhsexpr, IntEqual, BOOL_t, CallBIGEQ, BOOL_t, FALSENODE)
        # Not Equal Compare
        elif(op == COMPNOTEQUAL):
            t = self.explicateBinary(lhsexpr, rhsexpr, IntNotEqual, BOOL_t, CallBIGNEQ, BOOL_t, TRUENODE)
        elif(op == COMPIS):
            t = InjectFrom(BOOL_t, IntEqual((self.dispatch(lhsexpr),
                                             self.dispatch(rhsexpr))))
        # Error case
        else:
            raise Exception("explicate:unrecognized operation %s" % str(op))
        return t
    
    def visitAdd(self, n):
        lhsexpr = n.left
        rhsexpr = n.right
        t = self.explicateBinary(lhsexpr, rhsexpr, IntAdd, INT_t, CallBIGADD, BIG_t, CallTERROR([]))
        return t
    
    def visitNot(self, n):
        return IfExp(self.dispatch(n.expr), FALSENODE, TRUENODE)

    def visitUnarySub(self, n):
        varname = generate_name('let_us_expr')
        exprvar = Name(varname)
        t = Let(exprvar,
                self.dispatch(n.expr),
                IfExp(Or([IsTag(INT_t, exprvar),
                          IsTag(BOOL_t, exprvar)]),
                      InjectFrom(INT_t, IntUnarySub(ProjectTo(INT_t, exprvar))),
                      CallTERROR([])))
        return t

    # Explicate P1 Pyobj functions
    def visitCallFunc(self, n):
        # Verify/Rectify Names and Seperate Direct/Indirect Calls
        if(isinstance(n.node, Name)):
            args = []
            for arg in n.args:
                args += [self.dispatch(arg)]
            name = n.node.name
            if((name == "input") or (name == "input_int")):
                name = "input_int"
                output = CallFunc(Name(name), args)
            elif name in RESERVED_NAMES:
                output = CallFunc(Name(name), args)
            else:
                output = IndirectCallFunc(Name(name), args)
        else:
            node = self.dispatch(n.node)
            args = []
            for arg in n.args:
                args += [self.dispatch(arg)]
            output = IndirectCallFunc(node, args)
        return output

    def visitLambda(self, n):
        return SLambda(n.argnames, Stmt([Return(self.dispatch(n.code))]))

    def visitFunction(self, n):
        return Assign([AssName(n.name, 'OP_ASSIGN')],
                      SLambda(n.argnames, self.dispatch(n.code)))
