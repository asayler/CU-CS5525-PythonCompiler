from pyast import *
from vis import *

class ListVisitor(Visitor):
    visitModule = Module.list
    visitStmtList = StmtList.list
    visitDiscard = Discard.list
    visitIf = If.list
    visitClass = Class.list
    visitFunction = Function.list
    visitReturn = Return.list
    visitWhileFlat = WhileFlat.list
    visitWhile = While.list
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
    visitIntEqual = IntEqual.list
    visitIntNotEqual = IntNotEqual.list
    visitIntAdd = IntAdd.list
    visitIntUnarySub = IntUnarySub.list
    visitString = String.list
