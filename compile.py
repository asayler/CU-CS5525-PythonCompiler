#!/usr/bin/python

# Andy Sayler
# Fal 2012
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

DRAWAST_OFFSET = 13

def dim_nodes(n):
    """Function to count number of nodes in ast. Returns (total)"""
    
    if isinstance(n, Module):
        t = dim_nodes(n.node)
        return (1+t)
    elif isinstance(n, Stmt):
        total = 0
        for x in n.nodes:
            t = dim_nodes(x)
            total = total + t
        return (1+total)
    elif isinstance(n, Printnl):
        t = dim_nodes(n.nodes[0])
        return (1+t)
    elif isinstance(n, Assign):
        t0 = dim_nodes(n.nodes[0])
        t1 = dim_nodes(n.expr)
        return (1+t0+t1)
    elif isinstance(n, AssName):
        return (1)
    elif isinstance(n, Discard):
        t = dim_nodes(n.expr)
        return (1+t)
    elif isinstance(n, Const):
        return (1)
    elif isinstance(n, Name):
        return (1)
    elif isinstance(n, Add):
        t0 = dim_nodes(n.left)
        t1 = dim_nodes(n.right)
        return (1+t0+t1)
    elif isinstance(n, UnarySub):
        t = dim_nodes(n.expr)
        return (1+t)
    elif isinstance(n, CallFunc):
        t = dim_nodes(n.node)
        return (1+t)
    else:
        raise Exception('Error in dim_nodes: unrecognized AST node')

def del_dim(A, B):
    dimA = dim_nodes(A);
    dimB = dim_nodes(B);
    return ((dimA[0]-dimB[0]), (dimA[1]-dimB[1]), (dimA[2]-dimB[2]))

def astToList(n):
    """A Function to convert a standard AST tree to a list of lists of strings"""

    if isinstance(n, Module):
        return [n.__class__.__name__]+astToList(n.node)
    elif isinstance(n, Stmt):
        lsttmp = list()
        for x in n.nodes:
            lsttmp = lsttmp+[astToList(x)]
        return [n.__class__.__name__]+lsttmp
    elif isinstance(n, Printnl):
        lsttmp = list()
        for x in n.nodes:
            lsttmp = lsttmp+[astToList(x)]
        return [n.__class__.__name__]+lsttmp
    elif isinstance(n, Assign):
        lsttmp = list()
        for x in n.nodes:
            lsttmp = lsttmp+[astToList(x)]
        return [n.__class__.__name__]+lsttmp+[astToList(n.expr)]
    elif isinstance(n, AssName):
        return [n.__class__.__name__]
    elif isinstance(n, Discard):
        return [n.__class__.__name__]+astToList(n.expr)
    elif isinstance(n, Const):
        return [n.__class__.__name__]
    elif isinstance(n, Name):
        return [n.__class__.__name__]
    elif isinstance(n, Add):
        return [n.__class__.__name__]+[astToList(n.left)]+[astToList(n.right)]
    elif isinstance(n, UnarySub):
        return [n.__class__.__name__]+astToList(n.expr)
    elif isinstance(n, CallFunc):
        return [n.__class__.__name__]+astToList(n.node)
    else:
        raise Exception('Error in astToList: unrecognized AST node')

def drawAST(tree, offset="", term=0):
    """A Function to generate ASCII images of AST structures"""

    # Check input and convert to list of strings if necessary
    if isinstance(tree, compiler.ast.Module):
        tree = astToList(tree)
    elif(not(isinstance(tree, list))):
        raise Exception('Error in drawAST: tree must be a list or a Module')

    # Process list
    for i in range(len(tree)):
        if isinstance(tree[i], list):
            if(i < (len(tree) - 1)):
                #Terminal Branch
                drawAST(tree[i], (offset + "|".rjust(DRAWAST_OFFSET)))
            else:
                #Normal Branch
                drawAST(tree[i], (offset + " ".rjust(DRAWAST_OFFSET)))
        else:
            #Write Node
            sys.stderr.write(offset)
            if(i == 0 and len(offset) != 0):
                #First Node
                line = ""
                for j in range(DRAWAST_OFFSET-len(str(tree[i]))):
                    line = line+"-"
                sys.stderr.write((line+str(tree[i])).rjust(DRAWAST_OFFSET)+"\n")
            else:
                #Normal Node
                sys.stderr.write(str(tree[i]).rjust(DRAWAST_OFFSET)+"\n")

            #Write Seperator
            sys.stderr.write(offset)
            if(i < (len(tree) - 1)):
                #Last Node
                sys.stderr.write("|".rjust(DRAWAST_OFFSET)+"\n")
            else:
                #Normal Node
                sys.stderr.write(" ".rjust(DRAWAST_OFFSET)+"\n")

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

word_size = 4
def compile_stmt(ast, value_mode='movl'):
    """A function to compile an ast to x86"""
    global stack_map
    if isinstance(ast, Module):
        header = ['pushl %ebp',
                  'movl %esp, %ebp',
                  ('subl $%d, %%esp' % (len(scan_allocs(ast)) * word_size))]
        footer = ['movl $0, %eax', 'leave', 'ret']
        return header + compile_stmt(ast.node) + footer
    elif isinstance(ast, Stmt):
        return sum(map(compile_stmt, ast.nodes),[])
    elif isinstance(ast, Printnl):
        return compile_stmt(ast.nodes[0]) + ['pushl %eax',
                                             'call print_int_nl',
                                             ('addl $%d, %%esp' % word_size)]
    elif isinstance(ast, Assign):
        expr_assemb = compile_stmt(ast.expr)
        offset = allocate(ast.nodes[0].name, word_size)
        return expr_assemb + [('movl %%eax, -%d(%%ebp)' % offset)]
    elif isinstance(ast, Discard):
        return compile_stmt(ast.expr)
    elif isinstance(ast, Add):
        return compile_stmt(ast.left) + compile_stmt(ast.right, value_mode='addl')
    elif isinstance(ast, UnarySub):
        return ['negl %eax']
    elif isinstance(ast, CallFunc):
        return ['call input']
    elif isinstance(ast, Const):
        return [('%s $%d, %%eax' % (value_mode, ast.value))]
    elif isinstance(ast, Name):
        return [('%s -%d(%%ebp), %%eax' % (value_mode, stack_map[ast.name]))]
    else:
        raise Exception("Unexpected term: " + str(ast))

def write_to_file(assembly, outputFileName):
    """Function to write assembly to file"""
    assembly = '.globl main\nmain:\n\t' + '\n\t'.join(assembly)
    outputfile = open(outputFileName, 'w+')
    outputfile.write(assembly + '\n')
    outputfile.close()

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

    sys.stderr.write(str(argv[0]) + ": inputFilePath = " + inputFilePath + "\n")
    sys.stderr.write(str(argv[0]) + ": outputFilePath = " + str(outputFileName) + "\n")
    
    # Parse inputFile
    ast = compiler.parseFile(inputFilePath)
    
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
    assembly = compile_stmt(flatast)
    
    # Write output
    write_to_file(assembly, outputFileName)

    return 0

if __name__ == "__main__":
    sys.exit(main())
