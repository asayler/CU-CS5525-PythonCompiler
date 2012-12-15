# CU CS5525
# Fall 2012
# GSV Python Compiler
#
# copy_visitor.py
# Copy Visitor Prototype
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

class CopyVisitor(Visitor):
    visitProgram = Program.copy
    visitModule = Module.copy
    visitStmtList = StmtList.copy
    visitDiscard = Discard.copy
    visitIf = If.copy
    visitIfPhi = IfPhi.copy
    visitClass = Class.copy
    visitFunction = Function.copy
    visitReturn = Return.copy
    visitWhile = While.copy
    visitWhileFlat = WhileFlat.copy
    visitWhileFlatPhi = WhileFlatPhi.copy
    visitVarAssign = VarAssign.copy
    visitSubscriptAssign = SubscriptAssign.copy
    visitAttrAssign = AttrAssign.copy
    visitConst = Const.copy
    visitName = Name.copy
    visitGetAttr = GetAttr.copy
    visitCompare = Compare.copy
    visitLambda = Lambda.copy
    visitList = List.copy
    visitDict = Dict.copy
    visitSubscript = Subscript.copy
    visitAnd = And.copy
    visitOr = Or.copy
    visitAdd = Add.copy
    visitNot = Not.copy
    visitUnarySub = UnarySub.copy
    visitIfExp = IfExp.copy
    visitIfExpFlat = IfExpFlat.copy
    visitSLambda = SLambda.copy
    visitSLambdaLabel = SLambdaLabel.copy
    visitIndirectCallFunc = IndirectCallFunc.copy
    visitCallFunc = CallFunc.copy
    visitInstrSeq = InstrSeq.copy
    visitIsTag = IsTag.copy
    visitInjectFrom = InjectFrom.copy
    visitProjectTo = ProjectTo.copy
    visitLet = Let.copy
    visitIntCmp = IntCmp.copy
    visitIntAdd = IntAdd.copy
    visitIntUnarySub = IntUnarySub.copy
    visitString = String.copy
