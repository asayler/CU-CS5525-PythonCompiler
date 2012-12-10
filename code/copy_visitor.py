# CU CS5525
# Fall 2012
# Python Compiler
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
#    Andy Sayler
#       http://www.andysayler.com
#    Michael (Mike) Vitousek
#       http://csel.cs.colorado.edu/~mivi2269/

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
