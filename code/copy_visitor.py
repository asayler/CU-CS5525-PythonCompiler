from pyast import *
from vis import *

class CopyVisitor(Visitor):
    visitProgram = Program.copy
    visitModule = Module.copy
    visitStmtList = StmtList.copy
    visitDiscard = Discard.copy
    visitIf = If.copy
    visitClass = Class.copy
    visitFunction = Function.copy
    visitReturn = Return.copy
    visitWhileFlat = WhileFlat.copy
    visitWhile = While.copy
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
    visitIntEqual = IntEqual.copy
    visitIntNotEqual = IntNotEqual.copy
    visitIntAdd = IntAdd.copy
    visitIntUnarySub = IntUnarySub.copy
    visitString = String.copy
