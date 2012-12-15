# CU CS5525
# Fall 2012
# GSV Python Compiler
#
# list_visitor.py
# List Visitor Prototype
#
# Adopted from code by Jeremy Siek, Fall 2012
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

from pyast import *
from vis import *

class ListVisitor(Visitor):    
    visitProgram = Program.list
    visitModule = Module.list
    visitStmtList = StmtList.list
    visitDiscard = Discard.list
    visitIf = If.list
    visitIfPhi = IfPhi.list
    visitClass = Class.list
    visitFunction = Function.list
    visitReturn = Return.list
    visitWhile = While.list
    visitWhileFlat = WhileFlat.list
    visitWhileFlatPhi = WhileFlatPhi.list
    visitVarAssign = VarAssign.list
    visitSubscriptAssign = SubscriptAssign.list
    visitAttrAssign = AttrAssign.list
    visitConst = Const.list
    visitName = Name.list
    visitGetAttr = GetAttr.list
    visitCompare = Compare.list
    visitLambda = Lambda.list
    visitList = List.list
    visitDict = Dict.list
    visitSubscript = Subscript.list
    visitAnd = And.list
    visitOr = Or.list
    visitAdd = Add.list
    visitNot = Not.list
    visitUnarySub = UnarySub.list
    visitIfExp = IfExp.list
    visitIfExpFlat = IfExpFlat.list
    visitSLambda = SLambda.list
    visitSLambdaLabel = SLambdaLabel.list
    visitIndirectCallFunc = IndirectCallFunc.list
    visitCallFunc = CallFunc.list
    visitInstrSeq = InstrSeq.list
    visitIsTag = IsTag.list
    visitInjectFrom = InjectFrom.list
    visitProjectTo = ProjectTo.list
    visitLet = Let.list
    visitIntCmp = IntCmp.list
    visitIntAdd = IntAdd.list
    visitIntUnarySub = IntUnarySub.list
    visitString = String.list
