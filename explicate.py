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

class ExplicateVisitor(CopyVisitor):
    
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
        lhsname = generate_name('let_cmp_lhs')
        rhsname = generate_name('let_cmp_rhs')
        lhsvar = Name(lhsname)
        rhsvar = Name(rhsname)
        # Equal Compare
        if(n.ops[0][0] == COMPEQUAL):
            t = mono_Let(lhsvar,
                         self.dispatch(n.expr),
                         mono_Let(rhsvar,
                                  self.dispatch(n.ops[0][1]),
                                  IfExp(And([mono_IsTag(BOOL_t, lhsvar),
                                             mono_IsTag(BOOL_t, lhsvar)]),
                                        mono_InjectFrom(BOOL_t,
                                                        mono_IntEqual((mono_ProjectTo(BOOL_t,
                                                                                      lhsvar),
                                                                       mono_ProjectTo(BOOL_t,
                                                                                      rhsvar)))),
                                        IfExp(And([mono_IsTag(INT_t, lhsvar),
                                                   mono_IsTag(INT_t, rhsvar)]),
                                              mono_InjectFrom(BOOL_t,
                                                              mono_IntEqual((mono_ProjectTo(INT_t,
                                                                                            lhsvar),
                                                                             mono_ProjectTo(INT_t,
                                                                                            rhsvar)))),
                                              IfExp(And([mono_IsTag(BIG_t, lhsvar),
                                                         mono_IsTag(BIG_t, rhsvar)]),
                                                    mono_InjectFrom(BOOL_t,
                                                                    CallBIGEQ([mono_ProjectTo(BIG_t,
                                                                                              lhsvar),
                                                                               mono_ProjectTo(BIG_t,
                                                                                              rhsvar)])),
                                                    CallTERROR([]))))))
        # Not Equal Compare
        elif(n.ops[0][0] == COMPNOTEQUAL):
            t = mono_Let(lhsvar,
                         self.dispatch(n.expr),
                         mono_Let(rhsvar,
                                  self.dispatch(n.ops[0][1]),
                                  IfExp(And([mono_IsTag(BOOL_t, lhsvar),
                                             mono_IsTag(BOOL_t, lhsvar)]),
                                        mono_InjectFrom(BOOL_t,
                                                        mono_IntNotEqual((mono_ProjectTo(BOOL_t,
                                                                                         lhsvar),
                                                                          mono_ProjectTo(BOOL_t,
                                                                                         rhsvar)))),
                                        IfExp(And([mono_IsTag(INT_t, lhsvar),
                                                   mono_IsTag(INT_t, rhsvar)]),
                                              mono_InjectFrom(BOOL_t,
                                                              mono_IntNotEqual((mono_ProjectTo(INT_t,
                                                                                               lhsvar),
                                                                                mono_ProjectTo(INT_t,
                                                                                               rhsvar)))),
                                              IfExp(And([mono_IsTag(BIG_t, lhsvar),
                                                         mono_IsTag(BIG_t, rhsvar)]),
                                                    mono_InjectFrom(BOOL_t,
                                                                    CallBIGNEQ([mono_ProjectTo(BIG_t,
                                                                                               lhsvar),
                                                                                mono_ProjectTo(BIG_t,
                                                                                               rhsvar)])),
                                                    CallTERROR([]))))))
        # Error case
        else:
            raise Exception("explicate:unrecognized operation %s" % str(n.ops[0][0]))
        return t

    def visitAdd(self, n):
        lhsname = generate_name('let_add_lhs')
        rhsname = generate_name('let_add_rhs')
        lhsvar = Name(lhsname)
        rhsvar = Name(rhsname)
        t = mono_Let(lhsvar,
                     self.dispatch(n.left),
                     mono_Let(rhsvar,
                              self.dispatch(n.right),
                              IfExp(And([Or([mono_IsTag(INT_t, lhsvar),
                                             mono_IsTag(BOOL_t, lhsvar)]),
                                         Or([mono_IsTag(INT_t, rhsvar),
                                             mono_IsTag(BOOL_t, lhsvar)])]),
                                    mono_InjectFrom(INT_t, mono_IntAdd((mono_ProjectTo(INT_t,
                                                                                       lhsvar),
                                                                        mono_ProjectTo(INT_t,
                                                                                       rhsvar)))),
                                    IfExp(And([mono_IsTag(BIG_t, lhsvar),
                                               mono_IsTag(BIG_t, rhsvar)]),
                                          mono_InjectFrom(BIG_t, CallBIGADD([mono_ProjectTo(BIG_t,
                                                                                            lhsvar),
                                                                             mono_ProjectTo(BIG_t,
                                                                                            rhsvar)])),
                                          CallTERROR([])))))
        return t
        
    def visitNot(self, n):
        return Not(self.dispatch(n.expr), n.lineno)

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
