#!/usr/bin/python

# Andy Sayler
# CU CS5525
# Python Compiler

"""
USAGE:
    compile.py <file path>
"""
import sys
import compiler
from compiler.ast import *

DRAWAST_OFFSET = 15

def num_nodes(n):
    """Function to count number of nodes in ast. Returns (total, row, col)"""

    if isinstance(n, Module):
        t = num_nodes(n.node)
        return ((1+t[0]))
    elif isinstance(n, Stmt):
        cnt = 0
        for x in n.nodes:
            t = num_nodes(x)
            cnt = cnt + t[0]
        return ((1+cnt))
    elif isinstance(n, Printnl):
        return 1 + num_nodes(n.nodes[0])
    elif isinstance(n, Assign):
        return 1 + num_nodes(n.nodes[0]) + num_nodes(n.expr)
    elif isinstance(n, AssName):
        return 1
    elif isinstance(n, Discard):
        return 1 + num_nodes(n.expr)
    elif isinstance(n, Const):
        return 1
    elif isinstance(n, Name):
        return 1
    elif isinstance(n, Add):
        return 1 + num_nodes(n.left) + num_nodes(n.right)
    elif isinstance(n, UnarySub):
        return 1 + num_nodes(n.expr)
    elif isinstance(n, CallFunc):
        return 1 + num_nodes(n.node)
    else:
        raise Exception('Error in num_nodes: unrecognized AST node')

def unparse(n):
    raise Exception('Not yet implemented')

def drawast(n, offset=0, row=0, col=0):
    if isinstance(n, Module):
        print("Module".rjust(offset) + ": " + str(row) + "," + str(col))
        print("|".rjust(offset))
        drawast(n.node, offset, (row + 1), col)
    elif isinstance(n, Stmt):
        print("Stmt".rjust(offset) + ": " + str(row) + "," + str(col))
        cnt = 0
        for x in n.nodes:
            cnt = cnt + 1
            print("|".rjust(offset + cnt*DRAWAST_OFFSET))
        cnt = 0
        for x in n.nodes:
            cnt = cnt + 1
            drawast(x, (offset + cnt*DRAWAST_OFFSET), (row + 1), (col + cnt))
    elif isinstance(n, Printnl):
        print("Printnl".rjust(offset) + ": " + str(row) + "," + str(col))
        print("|".rjust(offset))
        drawast(n.nodes[0], offset, (row + 1), col)
    elif isinstance(n, Assign):
        print("Assign".rjust(offset) + ": " + str(row) + "," + str(col))
        print("|".rjust(offset))
        print("|".rjust(offset + DRAWAST_OFFSET))
        drawast(n.nodes[0], offset, (row + 1), col)
        drawast(n.expr, offset + DRAWAST_OFFSET, (row + 1), (col + 1))
    elif isinstance(n, AssName):
        print("AssName".rjust(offset) + ": " + str(row) + "," + str(col))
    elif isinstance(n, Discard):
        print("Discard",rjust(offset) + ": " + str(row) + "," + str(col))
        print("|".rjust(offset))
        drawast(n.expr, offset, (row + 1), col)
    elif isinstance(n, Const):
        print("Const".rjust(offset) + ": " + str(row) + "," + str(col))
    elif isinstance(n, Name):
        print("Name".rjust(offset) + ": " + str(row) + "," + str(col))
    elif isinstance(n, Add):
        print("Add".rjust(offset) + ": " + str(row) + "," + str(col))
        print("|".rjust(offset))
        print("|".rjust(offset + DRAWAST_OFFSET))
        drawast(n.left, offset, (row + 1), col)
        drawast(n.right, offset + DRAWAST_OFFSET, (row + 1), (col + 1))
    elif isinstance(n, UnarySub):
        print("UnarySub".rjust(offset) + ": " + str(row) + "," + str(col))
        print("|".rjust(offset))
        drawast(n.expr, offset, (row + 1), col)
    elif isinstance(n, CallFunc):
        print("CallFunc".rjust(offset) + ": " + str(row) + "," + str(col))
        print("|".rjust(offset))
        drawast(n.node, offset, (row + 1), col)
    else:
        raise Exception('Error in drawast: unrecognized AST node')


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
    sys.stderr.write(str(argv[0]) + ": inputFilePath = " + inputFilePath + "\n")
    
    # Parse inputFile
    ast = compiler.parseFile(inputFilePath)
    sys.stderr.write(str(argv[0]) + ": ast = " + str(ast) + "\n")

    #num = num_nodes(ast) work in progress to convert to touple-based function
    #sys.stderr.write(str(argv[0]) + ": num = " + str(num) + "\n")
    
    drawast(ast)

    return 0

if __name__ == "__main__":
    sys.exit(main())
