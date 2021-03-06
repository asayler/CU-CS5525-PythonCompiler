# CU CS5525
# Fall 2012
# GSV Python Compiler
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
#    Andrew (Andy) Sayler
#       http://www.andysayler.com
#    Michael (Mike) Vitousek
#       http://csel.cs.colorado.edu/~mivi2269/
#
# Copyright (c) 2012 by Anne Gatchell, Andy Sayler, and Mike Vitousek
#
# This file is part of the GSV CS5525 Fall 2012 Python Compiler.
#
#    The GSV CS5525 Fall 2012 Python Compiler is free software: you
#    can redistribute it and/or modify it under the terms of the GNU
#    General Public License as published by the Free Software
#    Foundation, either version 3 of the License, or (at your option)
#    any later version.
#
#    The GSV CS5525 Fall 2012 Python Compiler is distributed in the
#    hope that it will be useful, but WITHOUT ANY WARRANTY; without
#    even the implied warranty of MERCHANTABILITY or FITNESS FOR A
#    PARTICULAR PURPOSE.  See the GNU General Public License for more
#    details.
#
#    You should have received a copy of the GNU General Public License
#    along with the GSV CS5525 Fall 2012 Python Compiler.  If not, see
#    <http://www.gnu.org/licenses/>.

# Data Types
from pyast import *

# Parents
from copy_visitor import CopyVisitor

# Helper Types
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
COMPGT       = '>'
COMPGE       = '>='
COMPLT       = '<'
COMPLE       = '<='

class ExplicateVisitor(CopyVisitor):
    def __init__(self):
        super(ExplicateVisitor,self).__init__()
        
    # Helper Functions

    def projectType(self, expr):
        return IfExp(IsTag(BOOL_t, expr),
                     ProjectTo(BOOL_t, expr),
                     IfExp(IsTag(INT_t, expr),
                           ProjectTo(INT_t, expr),
                           ProjectTo(BIG_t, expr)))
    
    def explicateBinary(self, lhsexpr, rhsexpr,
                        smallFunc, smallType,
                        bigFunc, bigType,
                        mixedDefault, op=None):
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
                                     (smallFunc((self.projectType(lhsvar),
                                                self.projectType(rhsvar))))
                                     if op==None else 
                                     (smallFunc(op,
                                                (self.projectType(lhsvar),
                                                 self.projectType(rhsvar))))),
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
        return InjectFrom(INT_t, Const(n.value))

    def visitName(self, n):
        if(n.name == TRUENAME):
            return TRUENODE
        elif(n.name == FALSENAME):
            return FALSENODE
        else:
            return Name(n.name)

    # Non-Terminal Expressions
        
    def visitCompare(self, n):
        # Process Single Pair
        lhsexpr = n.expr
        op      = n.ops[0][0]
        rhsexpr = n.ops[0][1]
        if(op == COMPEQUAL):
            t = self.explicateBinary(lhsexpr, rhsexpr,
                                     IntCmp, BOOL_t,
                                     CallBIGEQ, BOOL_t,
                                     FALSENODE, PY_EQ)
        elif(op == COMPNOTEQUAL):
            t = self.explicateBinary(lhsexpr, rhsexpr,
                                     IntCmp, BOOL_t,
                                     CallBIGNEQ, BOOL_t,
                                     TRUENODE, PY_NE)
        elif(op == COMPGT):
            t = self.explicateBinary(lhsexpr, rhsexpr,
                                     IntCmp, BOOL_t,
                                     CallBIGGT, BOOL_t,
                                     CallGERROR([]), PY_GT)
        elif(op == COMPGE):
            t = self.explicateBinary(lhsexpr, rhsexpr,
                                     IntCmp, BOOL_t,
                                     CallBIGGE, BOOL_t,
                                     CallGERROR([]), PY_GE)
        elif(op == COMPLT):
            t = self.explicateBinary(lhsexpr, rhsexpr,
                                     IntCmp, BOOL_t,
                                     CallBIGLT, BOOL_t,
                                     CallGERROR([]), PY_LT)
        elif(op == COMPLE):
            t = self.explicateBinary(lhsexpr, rhsexpr,
                                     IntCmp, BOOL_t,
                                     CallBIGLE, BOOL_t,
                                     CallGERROR([]), PY_LE)
        elif(op == COMPIS):
            t = InjectFrom(BOOL_t, IntCmp(PY_EQ, (self.dispatch(lhsexpr),
                                                  self.dispatch(rhsexpr))))
        # Error case
        else:
            raise Exception("explicate:unrecognized operation %s" % str(op))
        return t
    
    def visitAdd(self, n):
        lhsexpr = n.left
        rhsexpr = n.right
        t = self.explicateBinary(lhsexpr, rhsexpr,
                                 IntAdd, INT_t,
                                 CallBIGADD, BIG_t,
                                 CallGERROR([]))
        return t
    
    def visitNot(self, n):
        return IfExp(self.dispatch(n.expr), FALSENODE, TRUENODE)

    def visitUnarySub(self, n):
        varname = generate_name('let_us_expr')
        exprvar = Name(varname)
        t = Let(exprvar,
                self.dispatch(n.expr),
                IfExp(IsTag(INT_t, exprvar),
                      InjectFrom(INT_t, IntUnarySub(ProjectTo(INT_t, exprvar))),
                      IfExp(IsTag(BOOL_t, exprvar),
                            InjectFrom(INT_t, IntUnarySub(ProjectTo(BOOL_t, exprvar))),
                            CallGERROR([]))))
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
            elif name == 'create_object' or name == 'create_class' or name == 'get_function' \
                    or name == 'get_receiver':
                output = InjectFrom(BIG_t, CallFunc(Name(name), args))
            elif name == 'is_class' or name == 'has_attr' or name == 'is_object' \
                    or name == 'is_bound_method' or name == 'is_unbound_method':
                output = InjectFrom(BOOL_t, CallFunc(Name(name), args))
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
        return SLambda(n.args, StmtList([Return(self.dispatch(n.expr))]))

    def visitFunction(self, n):
        return VarAssign(n.name,
                      SLambda(n.args, self.dispatch(n.code)))
