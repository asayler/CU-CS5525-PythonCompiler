#!/usr/bin/python

# Andy Sayler
# Fall 2012
# CU CS5525
# Python Compiler
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

"""
USAGE:
    compile.py <file path>
"""
import sys
import compiler
from compiler.ast import *

from x86ast import *

from astTools import *

import parser5525

debug = True

### Flatten Functions ###

temp_counter = -1
def new_temp(prefix):
    """A function to genertae unique temp var names"""
    global temp_counter
    temp_counter = temp_counter + 1
    return prefix + str(temp_counter)

def is_leaf(ast):
    """A function to return whether or not a node is a terminal leaf"""
    return isinstance(ast, Const) or isinstance(ast, Name)

def flattenAst(ast):
    """A function to flatten an AST"""

    if isinstance(ast, Module):
        #return a Module
        return Module(ast.doc, flattenAst(ast.node))
    elif isinstance(ast, Stmt):
        # Traverse list of nodes and flatten each
        nodes = []
        for n in ast.nodes:
            nodes.append(flattenAst(n))
        # Convert list of lists to flat list
        nodes = sum(nodes, [])
        # Return a Stmt
        return Stmt(nodes)
    elif isinstance(ast, Printnl):
        # Traverse list of nodes and flatten each
        nodes = []
        for n in ast.nodes:
            nodes.append(flattenAst(n))
        # Traverse flattened list and build (tree, list)
        prints = []
        for (t,l) in nodes:
            if not is_leaf(t):
                temp = new_temp('print')
                l.append(Assign([AssName(temp, 'OP_ASSIGN')], t))
                prints.append(Name(temp))
            else:
                prints.append(t)
        stmts = sum([l for (t, l) in nodes], [])
        return stmts + [Printnl(prints, ast.dest)]
    elif isinstance(ast, Assign):
        # Traverse list of nodes and flatten each
        nodes = []
        for n in ast.nodes:
            nodes.append(flattenAst(n))
        assigns = [t for (t, l) in nodes]
        stmts = sum([l for (t, l) in nodes], [])
        targ_node, targ_stmts = flattenAst(ast.expr)
        return stmts + targ_stmts + [Assign(assigns, targ_node)]
    elif isinstance(ast, AssName):
        return (ast, [])
    elif isinstance(ast, Discard):
        expr, stmts = flattenAst(ast.expr)
        return stmts + [Discard(expr)]
    elif isinstance(ast, Const):
        return (ast, [])
    elif isinstance(ast, Name):
        return (ast, [])
    elif isinstance(ast, Add):
        lexpr, lstmts = flattenAst(ast.left)
        rexpr, rstmts = flattenAst(ast.right)
        if not is_leaf(lexpr):
            temp = new_temp("left")
            lstmts.append(Assign([AssName(temp, 'OP_ASSIGN')], lexpr))
            lexpr = Name(temp)
        if not is_leaf(rexpr):
            temp = new_temp("right")
            rstmts.append(Assign([AssName(temp, 'OP_ASSIGN')], rexpr))
            rexpr = Name(temp)
        return (Add((lexpr, rexpr)), lstmts + rstmts)
    elif isinstance(ast, UnarySub):
        expr, stmts = flattenAst(ast.expr)
        if not is_leaf(expr):
            temp = new_temp("usub")
            stmts.append(Assign([AssName(temp, 'OP_ASSIGN')], expr))
            expr = Name(temp)
        return (UnarySub(expr), stmts)
    elif isinstance(ast, CallFunc):
        expr, stmts = flattenAst(ast.node)
        if not is_leaf(expr):
            temp = new_temp("func")
            stmts.append(Assign([AssName(temp, 'OP_ASSIGN')], expr))
            expr = Name(temp)
        args_exprs = []
        args_stmts = []
        for arg in ast.args:
            arg_expr, arg_stmts = flattenAst(arg)
            if not is_leaf(arg_expr):
                temp = new_temp("arg")
                arg_stmts.append(Assign([AssName(temp, 'OP_ASSIGN')], arg_expr))
                arg_expr = Name(temp)
            args_exprs.append(arg_expr)
            args_stmts = args_stmts + arg_stmts
        return (CallFunc(expr, args_exprs), stmts + args_stmts)
    else:
        raise Exception('Error in astToList: unrecognized AST node')

### Instruction Selection ###

def scan_allocs(ast):
    """A function to locate all unique assignments in an ast"""
    if isinstance(ast, Module):
        return scan_allocs(ast.node)
    elif isinstance(ast, Stmt):
        return reduce(lambda x,y: x.union(y), map(scan_allocs, ast.nodes), set([]))
    elif isinstance(ast, Assign):
        return reduce(lambda x,y: x.union(y), map(scan_allocs, ast.nodes), set([]))
    elif isinstance(ast, AssName):
        return set([ast.name])
    else:
        return set([])

current_offset = 0
stack_map = {}
def allocate(var, size):
    """A function to add a variable to the stack map"""
    global current_offset, stack_map
    if var in stack_map:
        return stack_map[var]
    current_offset = size + current_offset
    stack_map[var] = current_offset
    return current_offset

# Mike's Instruction Select
EAX = Reg86('eax')
EBP = Reg86('ebp')
ESP = Reg86('esp')
def instr_select(ast, value_mode=Move86):
    global stack_map
    if isinstance(ast, Module):
        return [Push86(EBP), Move86(ESP, EBP), Sub86(Const86(len(scan_allocs(ast)) * 4), ESP)] + instr_select(ast.node) + [Move86(Const86(0), EAX), Leave86(), Ret86()]
    elif isinstance(ast, Stmt):
        return sum(map(instr_select, ast.nodes),[])
    elif isinstance(ast, Printnl):
        return instr_select(ast.nodes[0]) + [Push86(EAX), Call86('print_int_nl'), Add86(Const86(4), ESP)]
    elif isinstance(ast, Assign):
        expr_assemb = instr_select(ast.expr)
        offset = allocate(ast.nodes[0].name, 4)
        return expr_assemb + [Move86(EAX, Mem86(offset, EBP))]
    elif isinstance(ast, Discard):
        return instr_select(ast.expr)
    elif isinstance(ast, Add):
        return instr_select(ast.left) + instr_select(ast.right, value_mode=Add86)
    elif isinstance(ast, UnarySub):
        return instr_select(ast.expr) + [Neg86(EAX)]
    elif isinstance(ast, CallFunc):
        return [Call86('input')]
    elif isinstance(ast, Const):
        return [value_mode(Const86(ast.value), EAX)]
    elif isinstance(ast, Name):
        return [value_mode(Mem86(stack_map[ast.name], EBP), EAX)]
    else:
        raise Exception("Unexpected term: " + str(ast))

def write_to_file(assembly, outputFileName):
    """Function to write assembly to file"""
    assembly = '.globl main\nmain:\n\t' + '\n\t'.join(assembly)
    outputfile = open(outputFileName, 'w+')
    outputfile.write(assembly + '\n')
    outputfile.close()

### Main Function ###

def main(argv=None):
    """Main Compiler Entry Point Function"""

    # Setup and Check Args
    if argv is None:
        argv = sys.argv
    if len(argv) != 2:
        sys.stderr.write(str(argv[0]) + " requires two arguments\n")
        sys.stderr.write(__doc__ + "\n")
        return 1
    inputFilePath = str(argv[1])
    if(inputFilePath[-3:] != ".py"):
        sys.stderr.write(str(argv[0]) + " input file must be of type *.py\n")
        return 1
    outputFilePath = inputFilePath.split('/')
    outputFileName = (outputFilePath[-1:])[0]
    outputFileName = outputFileName[:-3] + ".s"

#    sys.stderr.write(str(argv[0]) + ": inputFilePath = " + inputFilePath + "\n")
#    sys.stderr.write(str(argv[0]) + ": outputFilePath = " + str(outputFileName) + "\n")
    
    # Parse inputFile
#    ast = compiler.parseFile(inputFilePath)
    ast = parser5525.parseFile(inputFilePath)
#    sys.stderr.write("ast = " + str(ast) + "\n")
    
    # Measure Tree
#    sys.stderr.write(str(argv[0]) + ": dim_nodes(ast) = " + str(dim_nodes(ast)) + "\n")
#    sys.stderr.write(str(argv[0]) + ": allocs = " + str(len(scan_allocs(ast))) + "\n")

    # Draw Tree
#    drawAST(ast)
    
    # Flatten Tree
    flatast = flattenAst(ast)
#    print(ast)
#    print(flatast)

    # Measure Flat Tree
#   sys.stderr.write(str(argv[0]) + ": dim_nodes(ast) = " + str(dim_nodes(flatast)) + "\n")
#   sys.stderr.write(str(argv[0]) + ": allocs = " + str(len(scan_allocs(flatast))) + "\n")

    # Draw Flat Tree
#    drawAST(flatast)

    # Compile flat tree
    #assembly = compile_stmt(flatast)
    assembly = instr_select(flatast)
    
    # Write output
    write_to_file(map(str, assembly), outputFileName)

    return 0

if __name__ == "__main__":
    sys.exit(main())
