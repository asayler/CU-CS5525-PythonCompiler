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
import sys, compiler

# Data Types
from compiler.ast import *
from monoast import *
from x86ast import *

# Compiler Stages
from explicate import *
from flatten import *
from x86regalloc import *

# Helper Tools
from astTools import *
from graph_ast import *

debug = True

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

# Instruction Select

WORDLEN = 4
def instr_select_old(ast, value_mode=Move86):
    global stack_map
    if isinstance(ast, Module):
        return [Push86(EBP),
                Move86(ESP, EBP),
                Sub86(Const86(len(scan_allocs(ast)) * 4), ESP)]\
                + instr_select(ast.node)\
                + [Move86(Const86(0), EAX),
                   Leave86(),
                   Ret86()]
    elif isinstance(ast, Stmt):
        return sum(map(instr_select, ast.nodes),[])
    elif isinstance(ast, Printnl):
        return instr_select(ast.nodes[0])\
            + [Push86(EAX),
               Call86('print_int_nl'),
               Add86(Const86(4), ESP)]
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

def arg_select(ast):
    if isinstance(ast, Name):
        return Var86(ast.name)
    elif isinstance(ast, Const):
        return Const86(ast.value)
    else:
        raise Exception("Invalid argument: " + str(ast))

DISCARDTEMP = "discardtemp"
NULLTEMP = "nulltemp"

def instr_select(ast, writeTarget=NULLTEMP):
    if isinstance(ast, Module):
        return instr_select(ast.node)
    elif isinstance(ast, Stmt):
        return sum(map(instr_select, ast.nodes),[])
    elif isinstance(ast, Printnl):
        #TODO: Handle Callee Save Registers
        return [Push86(arg_select(ast.nodes[0])),
                Call86('print_int_nl'),
                Add86(Const86(WORDLEN), ESP)]
    elif isinstance(ast, Assign):
        return instr_select(ast.expr, Var86(ast.nodes[0].name))
    elif isinstance(ast, Discard):
        return instr_select(ast.expr, Var86(DISCARDTEMP))
    elif isinstance(ast, Add):
        return [Move86(arg_select(ast.left), writeTarget),
                Add86(arg_select(ast.right), writeTarget)]
    elif isinstance(ast, UnarySub):
        return [Move86(arg_select(ast.expr), writeTarget),
                Neg86(writeTarget)]
    elif isinstance(ast, CallFunc):
        #TODO: Handle Callee Save Registers
        return [Call86(ast.node.name),
                Move86(EAX, writeTarget)]
    elif isinstance(ast, Const):
        return [Move86(Const86(ast.value), writeTarget)]
    elif isinstance(ast, Name):
        return [Move86(Var86(ast.name), writeTarget)]
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
    if(debug):
        debugFileName = (outputFilePath[-1:])[0]
        debugFileName = debugFileName[:-3] + ".dot"

    if(debug):
        sys.stderr.write(str(argv[0]) + ": inputFilePath = " + inputFilePath + "\n")
        sys.stderr.write(str(argv[0]) + ": outputFilePath = " + str(outputFileName) + "\n")
    
    # Parse inputFile
    ast = compiler.parseFile(inputFilePath)
    if(debug):
        # Print AST
        sys.stderr.write("parsed ast = \n" + str(ast) + "\n")
        # Graph AST
        Graph_ast().writeGraph(ast, debugFileName)

    # Explicate
    monoast = ExplicateVisitor().preorder(ast)
    if(debug):
        # Print mono_AST
        sys.stderr.write("mono ast = \n" + str(monoast) + "\n")
        # Graph mono_AST
        #Graph_ast().writeGraph(monoast, debugFileName)        
        
    # Exit early since nothing past this point is implemented for p1 yet
    # return 0
    
    # Flatten Tree
    flatast = FlattenVisitor().preorder(monoast)
    if(debug):
        # Print flat_AST
        sys.stderr.write("flat ast = \n" + str(flatast) + "\n")


    # Compile flat tree
    assembly = instr_select(flatast)
    if(debug):
        sys.stderr.write("instr ast = \n" + "\n".join(map(str, assembly)) + "\n")

    # Reg Alloc
    if(debug):
        lafter = liveness(assembly)
        sys.stderr.write("lafter = \n" + "\n".join(map(str, lafter)) + "\n")
        graph = interference(assembly, lafter)
        sys.stderr.write("graph = " + str(graph) + "\n")
        colors = color(graph)
        sys.stderr.write("colors = " + str(colors) + "\n")
        (instrs, regOnlyVars) = fixMemToMem(assembly, colors)
        sys.stderr.write("regOnlyVars = " + str(regOnlyVars) + "\n")
        sys.stderr.write("instrs = \n" + "\n".join(map(str, instrs)) + "\n")


    assembly = regAlloc(assembly)
    if(debug):
        sys.stderr.write("instrs = \n" + "\n".join(map(str, assembly)) + "\n")

    # Write output
    write_to_file(map(str, assembly), outputFileName)

    return 0

if __name__ == "__main__":
    sys.exit(main())
