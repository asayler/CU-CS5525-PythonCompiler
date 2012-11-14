# UTILITY FUNCTIONS

def fst(plist):
    return sum(map(lambda (x, y): [x], plist), []) 
def snd(plist):
    return sum(map(lambda (x, y): y, plist), []) 
def map_dispatch(self, targets, *args):
    return map(lambda x: self.dispatch(x, *args), targets)
def binary(self, n, *args):
    return self.dispatch(n.left, *args) | self.dispatch(n.right, *args)
def accumulate(self, n, *args):
    return reduce(lambda x,y : x | y, map_dispatch(self, n, *args))
def list_dispatch(self, n, *args):
    return sum(map_dispatch(self, n, *args), [])

# TYPES

class PyType(object):
    """Class to represent type constants"""
    def __init__(self, typ):
        self.typ = typ
    def __repr__(self):
        return "MONOTYPE(%s)" % (self.typ)
    def __hash__(self):
        return hash(self.__repr__())
    def __eq__(self, that):
        return self.__repr__() == repr(that)

INT_t      = PyType('INT')
BOOL_t     = PyType('BOOL')
BIG_t      = PyType('BIGPYOBJ')

class PyNode(object):
    """Abstaract base class for monoast nodes"""
    valid_stages = []
    def __str__(self):
        return repr(self)
    def __repr__(self):
        return 'PyNode()'
    def __hash__(self):
        return hash(repr(self))
    def __eq__(self, that):
        return hash(repr(self)) == hash(repr(that))

    @staticmethod
    def copy(self, n, *args):
        ''' visitors for the CopyVisitor '''
        raise Exception('No valid copy visitor for ' + str(n.__class__))
    @staticmethod
    def list(self, n, *args):
        ''' visitors for list-generating visitors like Flatten and ClosureConvert'''
        raise Exception('No valid list generating copy visitor for ' + str(n.__class__))
    @staticmethod
    def find(self, n, *args):
        ''' Set-building visitor '''
        raise Exception('No valid set-building visitor for ' + str(n.__class__))

# MODULE

class Module(PyNode):
    def __init__(self, nodes):
        self.node = nodes
    def __repr__(self):
        return 'Module(%s)' % self.node
    @staticmethod
    def copy(self, n, *args):
        return Module(map_dispatch(self, n.nodes, *args))
    @staticmethod
    def list(self, n, *args):
        plist = map_dispatch(self, n.nodes, *args)
        nodes = []
        for node, ss in plist:
            nodes += ss + [node]
        return Module(nodes)
    @staticmethod
    def find(self, n, *args):
        return accumulate(self, n.nodes, *args)

# STATEMENTS

class Discard(PyNode):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return 'Discard(%s)' % self.expr
    @staticmethod
    def copy(self, n, *args):
        return Discard(self.dispatch(n.expr, *args))
    @staticmethod
    def list(self, n, *args):
        expr, ss = self.dispatch(n.expr, *args)
        return ss + [Discard(expr)]
    @staticmethod
    def find(self, n, *args):
        return self.dispatch(n.expr, *args)

class If(PyNode):
    def __init__(self, tests, else_):
        self.tests = tests
        self.else_ = else_
    def __repr__(self):
        return 'If(%s,%s)' % (self.tests, self.else_)
    @staticmethod
    def copy(self, n, *args):
        return If(map(lambda (x, y): (self.dispatch(x, *args), map_dispatch(self, y, *args))), map_dispatch(self, n.else_, *args))
    @staticmethod
    def list(self, n, *args):
        plist = map(lambda (x, y): (self.dispatch(x, *args), list_dispatch(self, y, *args)), n.tests)
        else_ = list_dispatch(self, n.else_, *args)
        tests = []
        ss = []
        for ((test, ssn), body) in plist:
            ss += [ssn]
            tests += [(test, body)]
        return ss + [If(tests, else_)]
    @staticmethod
    def find(self, n, *args):
        return accumulate(self, n.else_, *args) | reduce(lambda x,y: x | y, map(lambda (x,y): self.dispatch(x, *args) | accumulate(self, y, *args)))

class Class(PyNode):
    def __init__(self, name, bases, code):
        self.name = name 
        self.bases = bases
        self.code = code
    def __repr__(self):
        return 'Class(%s,%s,%s)' % (self.name, self.bases, self.code)

    @staticmethod
    def copy(self, n, *args):
        return Class(n.name, map_dispatch(self, n.bases, *args), map_dispatch(self, n.code, *args))
    @staticmethod
    def list(self, n, *args):
        plist = map_dispatch(self, n.bases, *args)
        code = list_dispatch(self, n.code, *args)
        return snd(plist) + [Class(n.name, fst(plist), code)]
    @staticmethod
    def find(self, n, *args):
        return accumulate(self, n.bases, *args) | accumulate(self, n.code, *args)

class Function(PyNode):
    def __init__(self, name, args, code):
        self.name = name
        self.args = args
        self.code = code
    def __repr__(self):
        return 'Function(%s,%s,%s)' % (self.name, self.args, self.code)

    @staticmethod
    def copy(self, n, *args):
        return Function(n.name, n.args, map_dispatch(self, n.code, *args))
    @staticmethod
    def list(self, n, *args):
        return [Function(n.name, n.args, list_dispatch(self, n.code, *args))]
    @staticmethod
    def find(self, n, *args):
        return accumulate(self, n.code, *args)

class Return(PyNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'Return(%s)' % self.value

    @staticmethod
    def copy(self, n, *args):
        return Return(self.dispatch(n.value, *args))
    @staticmethod
    def list(self, n, *args):
        value, ss = self.dispatch(n.value, *args)
        return ss + [Return(value)]
    @staticmethod
    def find(self, n, *args):
        return self.dispatch(n.value, *args)


class WhileFlat(PyNode):
    def __init__(self, testss, test, body, else_):
        self.testss = testss
        self.test = test
        self.body = body
        self.else_ = else_
    def __repr__(self):
        return "WhileFlat(%s ,%s, %s, %s)" % (repr(self.testss), repr(self.test),
                                              repr(self.body), repr(self.else_))
    @staticmethod
    def copy(self, n, *args):
        return WhileFlat(self.dispatch(n.testss, *args),
                         self.dispatch(n.test, *args),
                         self.dispatch(n.body, *args),
                         self.dispatch(n.else_, *args) if n.else_ else n.else_)
    @staticmethod
    def list(self, n, *args):
        testss = self.dispatch(n.testss, *args)
        test, ss = self.dispatch(n.test, *args),
        return [WhileFlat(testss + ss
                         test,
                         self.dispatch(n.body, *args),
                         self.dispatch(n.else_, *args) if n.else_ else n.else_)]
    @staticmethod
    def find(self, n, *args):
        return self.dispatch(n.testss, *args) | self.dispatch(n.test, *args) | self.dispatch(n.body, *args) | (self.dispatch(n.else_, *args) if n.else_ else set([]))

class VarAssign(PyNode):
    def __init__(self, target, value):
        self.target = target
        self.value = value
    def __repr__(self):
        return "VarAssign(%s, %s)" % (repr(self.target), repr(self.value))
    @staticmethod
    def copy(self, n, *args):
        return VarAssign(self.dispatch(n.target, *args), self.dispatch(n.value, *args))
    @staticmethod
    def list(self, n, *args):
        target, ss1 = self.dispatch(n.target, *args)
        value, ss2 = self.dispatch(n.value, *args)
        return ss1 + ss2 + ss3 + [VarAssign(target, value)]
    @staticmethod
    def find(self, n, *args):
        return self.dispatch(n.target, *args) | self.dispatch(n.value, *args)

class SubscriptAssign:
    '''Assignment statement for subscription'''
    def __init__(self, target, sub, value):
        self.target = target
        self.sub = sub
        self.value = value
    def __repr__(self):
        return "SubscriptAssign(%s, %s, %s)" % (repr(self.target), repr(self.sub), repr(self.value))
    @staticmethod
    def copy(self, n, *args):
        return SubscriptAssign(self.dispatch(n.target, *args), self.dispatch(n.sub, *args), self.dispatch(n.value, *args))
    @staticmethod
    def list(self, n, *args):
        target, ss1 = self.dispatch(n.target, *args)
        value, ss2 = self.dispatch(n.value, *args)
        sub, ss3 = self.dispatch(n.sub, *args)
        return ss1 + ss2 + ss3 + [SubscriptAssign(target, sub, value)]
    @staticmethod
    def find(self, n, *args):
        return self.dispatch(n.target, *args) | self.dispatch(n.value, *args) | self.dispatch(n.sub, *args)

class AttrAssign:
    '''Assignment statement for attributes'''
    def __init__(self, target, attr, value):
        self.target = target
        self.attr = attr
        self.value = value
    def __repr__(self):
        return "AttrAssign(%s, %s, %s)" % (repr(self.target), repr(self.attr), repr(self.value))
    @staticmethod
    def copy(self, n, *args):
        return AttrAssign(self.dispatch(n.target, *args), n.attr, self.dispatch(n.value, *args))
    @staticmethod
    def list(self, n, *args):
        target, ss1 = self.dispatch(n.target, *args)
        value, ss2 = self.dispatch(n.value, *args)
        return ss1 + ss2 + [AttrAssign(target, n.attr, value)]
    @staticmethod
    def find(self, n, *args):
        return self.dispatch(n.target, *args) | self.dispatch(n.value, *args)

# EXPRESSIONS


class Const(PyNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'Const(%d)' % self.value

    @staticmethod
    def copy(self, n, *args):
        return Const(n.value)
    @staticmethod
    def list(self, n, *args):
        return (Const(n.value), [])
    @staticmethod
    def find(self, n, *args):
        return set([])

class Name(PyNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return 'Name(%s)' % self.name

    @staticmethod
    def copy(self, n, *args):
        return Name(n.name)
    @staticmethod
    def list(self, n, *args):
        return (Name(n.name), [])
    @staticmethod
    def find(self, n, *args):
        return set([])

 # NEXT IS GETATTR #

class SLambda(PyNode):
    def __init__(self, params, code, label=None):
        self.params = params
        self.code = code
        self.label = label        
    def __repr__(self):
        return 'SLambda(%s, %s, %s)' % (self.params, self.code, self.label) 
    @staticmethod
    def copy(self, n, *args):
        return SLambda(n.params, self.dispatch(n.code, *args), n.label)
    @staticmethod
    def list(self, n, *args):
        return (SLambda(n.params, self.dispatch(code, *args), n.label), [])
    @staticmethod
    def find(self, n, *args):
        return self.dispatch(n.code, *args)

class SLambdaLabel(PyNode):
    def __init__(self, name):
        self.name = name
                
    def __repr__(self):
        return 'SLambdaLabel(%s)' % (self.name) 
    @staticmethod
    def copy(self, n, *args):
        return SLambdaLabel(n.name)
    @staticmethod
    def list(self, n, *args):
        return (SLambdaLabel(n.name), [])
    @staticmethod
    def find(self, n, *args):
        return set([])

class IndirectCallFunc(PyNode):
    def __init__(self, node, args):
        self.node = node
        self.args = args
    def __repr__(self):
        return 'IndirectCallFunc(%s, %s)' % (self.node, self.args)
    @staticmethod
    def copy(self, n, *args):
        return IndirectCallFunc(self.dispatch(n.node, args, *args), map_dispatch(self, n.args, *args))
    @staticmethod
    def list(self, n, *args):
        (node, ss) = self.dispatch(node, *args)
        plist = map_dispatch(self, n.args, *args)
        return (IndirectCallFunc(node, fst(plist)), ss + snd(plist))
    @staticmethod
    def find(self, n, *args):
        return self.dispatch(n.node, *args) | reduce(lambda x,y: x | y, 
                                                     map_dispatch(self, n.args, *args), 
                                                     set([]))

class InstrSeq(PyNode):
    def __init__(self, nodes, expr):
        self.nodes = nodes
        self.expr = expr
    def __repr__(self):
        return "InstrSeq(%s, %s)" % (repr(self.nodes), repr(self.expr))
    @staticmethod
    def copy(self, n, *args):
        return InstrSeq(map_dispatch(self, nodes, *args), self.dispatch(n.expr, *args))
    @staticmethod
    def list(self, n, *args):
        expr, ss = self.dispatch(n.expr, *args)
        return (InstrSeq(sum(map_dispatch(self, nodes, *args), []) + ss, expr), [])
    @staticmethod
    def find(self, n, *args):
        return self.dispatch(n.expr, *args) | reduce(lambda x,y: x | y, 
                                              map_dispatch(self, n.nodes, *args), 
                                              set([]))

class IsTag(PyNode):
    """Call code to determine if 'arg' is of type 'typ'"""
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
    def __repr__(self):
        return "IsTag(%s, %s)" % (repr(self.typ), repr(self.arg))
    @staticmethod
    def copy(self, n, *args):
        return IsTag(n.typ, self.dispatch(n.arg, *args))
    @staticmethod
    def list(self, n, *args):
        arg, ss = self.dispatch(n.arg, *args)
        return (IsTag(n.typ, arg), ss)
    @staticmethod
    def find(self, n, *args):
        return self.dispatch(n.arg, *args)

class InjectFrom(PyNode):
    """Convert result of 'arg' from 'typ' to pyobj"""
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
    def __repr__(self):
        return "InjectFrom(%s, %s)" % (repr(self.typ), repr(self.arg))
    @staticmethod
    def copy(self, n, *args):
        return InjectFrom(n.typ, self.dispatch(n.arg, *args))
    @staticmethod
    def list(self, n, *args):
        arg, ss = self.dispatch(n.arg, *args)
        return (InjectFrom(n.typ, arg), ss)
    @staticmethod
    def find(self, n, *args):
        return self.dispatch(n.arg, *args)

class ProjectTo(PyNode):
    """Convert result of 'arg' from pyobj to 'typ'"""
    def __init__(self, typ, arg):
        self.typ = typ
        self.arg = arg
    def __repr__(self):
        return "ProjectTo(%s, %s)" % (repr(self.typ), repr(self.arg))
    @staticmethod
    def copy(self, n, *args):
        return ProjectTo(n.typ, self.dispatch(n.arg, *args))
    @staticmethod
    def list(self, n, *args):
        arg, ss = self.dispatch(n.arg, *args)
        return (ProjectTo(n.typ, arg), ss)
    @staticmethod
    def find(self, n, *args):
        return self.dispatch(n.arg, *args)

class Let(PyNode):
    """Evaluate 'var' = 'rhs', than run body referencing 'var'"""
    def __init__(self, var, rhs, body):
        self.var  = var
        self.rhs  = rhs
        self.body = body
    def __repr__(self):
        return "Let(%s, %s, %s)" % (repr(self.var), repr(self.rhs), repr(self.body))
    @staticmethod
    def copy(self, n, *args):
        return Let(self.dispatch(n.var, *args), self.dispatch(n.rhs, *args), self.dispatch(n.body, *args))
    @staticmethod
    def list(self, n, *args):
        var, ss1 = self.dispatch(n.var, *args)
        rhs, ss2 = self.dispatch(n.rhs, *args)
        body, ss3 = self.dispatch(n.body, *args)
        return (Let(var, rhs, body), ss1 + ss2 + ss3)
    @staticmethod
    def find(self, n, *args):
        return self.dispatch(n.var, *args) | self.dispatch(n.rhs, *args) | self.dispatch(n.body, *args)

class IntEqual(PyNode):
    def __init__(self, (left, right)):
        self.left = left
        self.right = right
    def __repr__(self):
        return "IntEqual(%s, %s)" % (repr(self.left), repr(self.right))
    @staticmethod
    def copy(self, n, *args):
        return IntEqual((self.dispatch(n.left, *args), self.dispatch(n.right, *args)))
    @staticmethod
    def list(self, n, *args):
        left, ss1 = self.dispatch(n.left, *args)
        right, ss2 = self.dispatch(n.right, *args)
        return (IntEqual((left, right)), ss1 + ss2)
    @staticmethod
    def find(self, n, *args):
        return binary(self, n, *args)

class IntNotEqual(PyNode):
    def __init__(self, (left, right)):
        self.left = left
        self.right = right
    def __repr__(self):
        return "IntNotEqual(%s, %s)" % (repr(self.left), repr(self.right))
    @staticmethod
    def copy(self, n, *args):
        return IntNotEqual((self.dispatch(n.left, *args), self.dispatch(n.right, *args)))
    @staticmethod
    def list(self, n, *args):
        left, ss1 = self.dispatch(n.left, *args)
        right, ss2 = self.dispatch(n.right, *args)
        return (IntNotEqual((left, right)), ss1 + ss2)
    @staticmethod
    def find(self, n, *args):
        return binary(self, n, *args)

class IntAdd(PyNode):
    def __init__(self, (left, right)):
        self.left = left
        self.right = right
    def __repr__(self):
        return "IntAdd((%s, %s))" % (repr(self.left), repr(self.right))
    @staticmethod
    def copy(self, n, *args):
        return IntAdd((self.dispatch(n.left, *args), self.dispatch(n.right, *args)))
    @staticmethod
    def list(self, n, *args):
        left, ss1 = self.dispatch(n.left, *args)
        right, ss2 = self.dispatch(n.right, *args)
        return (IntAdd((left, right)), ss1 + ss2)
    @staticmethod
    def find(self, n, *args):
        return binary(self, n, *args)

class IntUnarySub(PyNode):
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self):
        return "IntUnarySub(%s)" % (repr(self.expr))
    @staticmethod
    def copy(self, n, *args):
        return IntUnarySub(self.dispatch(n.expr, *args))
    @staticmethod
    def list(self, n, *args):
        expr, ss = self.dispatch(n.expr, *args)
        return (IntUnarySub(expr), ss)
    @staticmethod
    def find(self, n, *args):
        return self.dispatch(n.expr, *args)

class String(PyNode):
    def __init__(self, string):
        self.string = string
    def __repr__(self):
        return 'String(%s)' % self.string
    @staticmethod
    def copy(self, n, *args):
        return String(n.string)
    @staticmethod
    def list(self, n, *args):
        return (String(n.string), [])
    @staticmethod
    def find(self, n, *args):
        return set([])
