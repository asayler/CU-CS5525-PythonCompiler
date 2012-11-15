# CU CS5525
# Fall 2012
# Python Compiler
#
# instr_select.py
# Visitor Funcations for x86 Instruction Selection
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

# Helper Tools
from vis import Visitor

class SetVisitor(Visitor):
    visitProgram = Program.find
    visitModule = Module.find    
    visitStmtList = StmtList.find
    visitDiscard = Discard.find
    visitIf = If.find
    visitClass = Class.find
    visitFunction = Function.find
    visitReturn = Return.find
    visitWhileFlat = WhileFlat.find
    visitWhile = While.find
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
    visitIntEqual = IntEqual.find
    visitIntNotEqual = IntNotEqual.find
    visitIntAdd = IntAdd.find
    visitIntUnarySub = IntUnarySub.find
    visitString = String.find
