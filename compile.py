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
    """Function to count number of nodes in ast. Returns (total, rows, cols)"""

    if isinstance(n, Module):
        t = num_nodes(n.node)
        return ((1+t[0]), 1+t[1], t[2])
    elif isinstance(n, Stmt):
        total = 0
        col = 0
        row = 0;
        for x in n.nodes:
            t = num_nodes(x)
            total = total + t[0]
            col = max(col, t[1])
            row = max(row, t[1])
        return (1+total, 1+row, 1+col)
    elif isinstance(n, Printnl):
        t = num_nodes(n.nodes[0])
        return (1+t[0], 1+t[1], t[2])
    elif isinstance(n, Assign):
        t0 = num_nodes(n.nodes[0])
        t1 = num_nodes(n.expr)
        return ((1+t0[0]+t1[0]), 1+max(t0[1], t1[1]), 1+max(t0[2], t1[2]))
    elif isinstance(n, AssName):
        return (1, 1, 1)
    elif isinstance(n, Discard):
        t = num_nodes(n.expr)
        return ((1+t[0]), 1+t[1], t[2])
    elif isinstance(n, Const):
        return (1, 1, 1)
    elif isinstance(n, Name):
        return (1, 1, 1)
    elif isinstance(n, Add):
        t0 = num_nodes(n.left)
        t1 = num_nodes(n.right)
        return (1+t0[0]+t1[0], 1+max(t0[1], t1[1]), 1+max(t0[2], t1[2]))
    elif isinstance(n, UnarySub):
        t = num_nodes(n.expr)
        return (1+t[0], 1+t[1], t[2])
    elif isinstance(n, CallFunc):
        t = num_nodes(n.node)
        return (1+t[0], 1+t[1], t[2])
    else:
        raise Exception('Error in num_nodes: unrecognized AST node')

def unparse(n):
    raise Exception('Not yet implemented')

def drawast(n, offset=0, row=0, col=0, output=None):
    
    if isinstance(n, Module):
        output[row][col] = "Module"
        drawast(n.node, offset, (row + 1), col, output)
    elif isinstance(n, Stmt):
        output[row][col] = "Stmt"
        cnt = 0
        for x in n.nodes:
            cnt = cnt + 1
            #TODO: Bug here, does not account for children with more than 1 col...
            drawast(x, (offset + cnt*DRAWAST_OFFSET), (row + 1), (col + cnt), output)
    elif isinstance(n, Printnl):
        output[row][col] = "Printnl"
        drawast(n.nodes[0], offset, (row + 1), col, output)
    elif isinstance(n, Assign):
        output[row][col] = "Assign"
        drawast(n.nodes[0], offset, (row + 1), col, output)
        drawast(n.expr, offset + DRAWAST_OFFSET, (row + 1), (col + 1), output)
    elif isinstance(n, AssName):
        output[row][col] = "AssName"
    elif isinstance(n, Discard):
        output[row][col] = "Discard"
        drawast(n.expr, offset, (row + 1), col, output)
    elif isinstance(n, Const):
        output[row][col] = "Const"
    elif isinstance(n, Name):
        output[row][col] = "Name"
    elif isinstance(n, Add):
        output[row][col] = "Add"
        drawast(n.left, offset, (row + 1), col, output)
        drawast(n.right, offset + DRAWAST_OFFSET, (row + 1), (col + 1), output)
    elif isinstance(n, UnarySub):
        output[row][col] = "UnarySub"
        drawast(n.expr, offset, (row + 1), col, output)
    elif isinstance(n, CallFunc):
        output[row][col] = "CallFunc"
        drawast(n.node, offset, (row + 1), col, output)
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

    num = num_nodes(ast)
    sys.stderr.write(str(argv[0]) + ": num = " + str(num) + "\n")
    
    # Draw Tree
    dim = num_nodes(ast);
    output = [["" for i in range(dim[2])] for j in range(dim[1])]
    drawast(ast, 0, 0, 0, output)
    for i in range(dim[1]):
        for j in range(dim[2]):
            sys.stderr.write(output[i][j].rjust(DRAWAST_OFFSET))
        sys.stderr.write("\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())
