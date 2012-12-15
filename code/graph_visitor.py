# CU CS5525
# Fall 2012
# GSV Python Compiler
#
# graph_visitor.py
# Functions to produce an GraphViz dot graph from AST
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
from graphvis_dot import Graphvis_dot

class GraphVisitor(Visitor):

    def writeGraph(self, ast, filepath):
        lines = self.preorder(ast)
        Graphvis_dot().drawGraph(lines, filepath)

    visitProgram = Program.graph
    visitModule = Module.graph
    visitStmtList = StmtList.graph
    visitDiscard = Discard.graph
    visitIf = If.graph
    visitIfPhi = IfPhi.graph
    visitClass = Class.graph
    visitFunction = Function.graph
    visitReturn = Return.graph
    visitWhile = While.graph
    visitWhileFlat = WhileFlat.graph
    visitWhileFlatPhi = WhileFlatPhi.graph
    visitVarAssign = VarAssign.graph
    visitSubscriptAssign = SubscriptAssign.graph
    visitAttrAssign = AttrAssign.graph
    visitConst = Const.graph
    visitName = Name.graph
    visitGetAttr = GetAttr.graph
    visitCompare = Compare.graph
    visitLambda = Lambda.graph
    visitList = List.graph
    visitDict = Dict.graph
    visitSubscript = Subscript.graph
    visitAnd = And.graph
    visitOr = Or.graph
    visitAdd = Add.graph
    visitNot = Not.graph
    visitUnarySub = UnarySub.graph
    visitIfExp = IfExp.graph
    visitIfExpFlat = IfExpFlat.graph
    visitSLambda = SLambda.graph
    visitSLambdaLabel = SLambdaLabel.graph
    visitIndirectCallFunc = IndirectCallFunc.graph
    visitCallFunc = CallFunc.graph
    visitInstrSeq = InstrSeq.graph
    visitIsTag = IsTag.graph
    visitInjectFrom = InjectFrom.graph
    visitProjectTo = ProjectTo.graph
    visitLet = Let.graph
    visitIntCmp = IntCmp.graph
    visitIntAdd = IntAdd.graph
    visitIntUnarySub = IntUnarySub.graph
    visitString = String.graph
