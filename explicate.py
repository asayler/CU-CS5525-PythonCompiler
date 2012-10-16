#!/usr/bin/python

# Andy Sayler
# Fall 2012
# CU CS5525
# explicate visitor functions
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

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

COMPEQUAL    = '=='
COMPNOTEQUAL = '!='
COMPIS       = 'is'

class ExplicateVisitor(CopyVisitor):
  
    # Helper Functions

    def projectType(self, expr):
        return IfExp(mono_IsTag(BOOL_t, expr),
                     mono_ProjectTo(BOOL_t, expr),
                     IfExp(mono_IsTag(INT_t, expr),
                           mono_ProjectTo(INT_t, expr),
                           mono_ProjectTo(BIG_t, expr)))
                     
    def explicateBinary(self, lhsexpr, rhsexpr, smallFunc, smallType, bigFunc, bigType):
        lhsname = generate_name('let_binexp_lhs')
        rhsname = generate_name('let_binexp_rhs')
        lhsvar = Name(lhsname)
        rhsvar = Name(rhsname)
        t = mono_Let(lhsvar,
                     self.dispatch(lhsexpr),
                     mono_Let(rhsvar,
                              self.dispatch(rhsexpr),
                              # Small-Small Case
                              IfExp(And([Or([mono_IsTag(BOOL_t, lhsvar),
                                             mono_IsTag(INT_t, lhsvar)]),
                                         Or([mono_IsTag(BOOL_t, rhsvar),
                                             mono_IsTag(INT_t, rhsvar)])]),
                                    mono_InjectFrom(smallType,
                                                    smallFunc((self.projectType(lhsvar),
                                                               self.projectType(rhsvar)))),
                                    # Big-Big Case
                                    IfExp(And([mono_IsTag(BIG_t, lhsvar),
                                               mono_IsTag(BIG_t, rhsvar)]),
                                          mono_InjectFrom(bigType,
                                                          bigFunc([self.projectType(lhsvar),
                                                                   self.projectType(rhsvar)])),
                                          # Mixed Case
                                          # TODO: Add mixed case logic
                                          CallTERROR([])))))
        return t

    # Terminal Expressions

    def visitConst(self, n):
        return mono_InjectFrom(INT_t, Const(n.value, n.lineno))

    def visitName(self, n):
        if(n.name == TRUENAME):
            return mono_InjectFrom(BOOL_t, Const(TRUEVALUE, n.lineno))
        elif(n.name == FALSENAME):
            return mono_InjectFrom(BOOL_t, Const(FALSEVALUE, n.lineno))
        else:
            return Name(n.name, n.lineno)

    # Non-Terminal Expressions

    def visitList(self, n):
        raise Exception("Lists not yet implemented")

    def visitDict(self, n):
        raise Exception("Dicts not yet implemented")

    def visitSubscript(self, n):
        raise Exception("Subscript not yet implemented")

    def visitCompare(self, n):
        # Process Single Pair
        lhsexpr = n.expr
        op      = n.ops[0][0]
        rhsexpr = n.ops[0][1]
        # Equal Compare
        if(op == COMPEQUAL):
            t = self.explicateBinary(lhsexpr, rhsexpr, mono_IntEqual, BOOL_t, CallBIGEQ, BOOL_t)
        # Not Equal Compare
        elif(op == COMPNOTEQUAL):
            t = self.explicateBinary(lhsexpr, rhsexpr, mono_IntNotEqual, BOOL_t, CallBIGNEQ, BOOL_t)
        elif(op == COMPIS):
            raise Exception("Compare('is') not yet implemented")
        # Error case
        else:
            raise Exception("explicate:unrecognized operation %s" % str(op))
        return t
  
    def visitAdd(self, n):
        lhsexpr = n.left
        rhsexpr = n.right
        t = self.explicateBinary(lhsexpr, rhsexpr, mono_IntAdd, INT_t, CallBIGADD, BIG_t)
        return t
        
    def visitNot(self, n):
        raise Exception("Not not yet implemented")

    def visitUnarySub(self, n):
        varname = generate_name('let_us_expr')
        exprvar = Name(varname)
        t = mono_Let(exprvar,
                     self.dispatch(n.expr),
                     IfExp(Or([mono_IsTag(INT_t, exprvar),
                               mono_IsTag(BOOL_t, exprvar)]),
                           mono_InjectFrom(INT_t, mono_IntUnarySub(mono_ProjectTo(INT_t, exprvar))),
                           CallTERROR([])))
        return t

    # Explicate P1 Pyobj functions
    def visitCallFunc(self, n):
        args = []
        # Verify/Rectify Names
        if(isinstance(n.node, Name)):
            name = n.node.name
            if(name == "input"):
                name = "input_int"
            elif(name == "input_int"):
                pass
            else:
                raise Exception("Only input function accepted in p1")
            newName = Name(name)
        else:
            raise Exception("Only named functions accepted in p1")
        #Copy Function
        for arg in n.args:
            args += [self.dispatch(arg)]
        return CallFunc(newName, args, n.star_args, n.dstar_args, n.lineno)
