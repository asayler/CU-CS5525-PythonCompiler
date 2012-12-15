# CU CS5525
# Fall 2012
# GSV Python Compiler
#
# set_visitor.py
# Set Visitor Prototype
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

# Helper Tools
from vis import Visitor

class SetVisitor(Visitor):
    visitProgram = Program.find
    visitModule = Module.find    
    visitStmtList = StmtList.find
    visitDiscard = Discard.find
    visitIf = If.find
    visitIfPhi = IfPhi.find
    visitClass = Class.find
    visitFunction = Function.find
    visitReturn = Return.find
    visitWhile = While.find
    visitWhileFlat = WhileFlat.find
    visitWhileFlatPhi = WhileFlatPhi.find
    visitVarAssign = VarAssign.find
    visitSubscriptAssign = SubscriptAssign.find
    visitAttrAssign = AttrAssign.find
    visitConst = Const.find
    visitName = Name.find
    visitGetAttr = GetAttr.find
    visitCompare = Compare.find
    visitLambda = Lambda.find
    visitList = List.find
    visitDict = Dict.find
    visitSubscript = Subscript.find
    visitAnd = And.find
    visitOr = Or.find
    visitAdd = Add.find
    visitNot = Not.find
    visitUnarySub = UnarySub.find
    visitIfExp = IfExp.find
    visitIfExpFlat = IfExpFlat.find
    visitSLambda = SLambda.find
    visitSLambdaLabel = SLambdaLabel.find
    visitIndirectCallFunc = IndirectCallFunc.find
    visitCallFunc = CallFunc.find
    visitInstrSeq = InstrSeq.find
    visitIsTag = IsTag.find
    visitInjectFrom = InjectFrom.find
    visitProjectTo = ProjectTo.find
    visitLet = Let.find
    visitIntCmp = IntCmp.find
    visitIntAdd = IntAdd.find
    visitIntUnarySub = IntUnarySub.find
    visitString = String.find
