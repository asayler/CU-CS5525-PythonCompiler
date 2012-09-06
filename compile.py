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

def dim_nodes(n):
    """Function to count number of nodes in ast. Returns (total, rows, cols)"""

    if isinstance(n, Module):
        t = dim_nodes(n.node)
        return ((1+t[0]), 1+t[1], t[2])
    elif isinstance(n, Stmt):
        total = 0
        col = 0
        row = 0;
        for x in n.nodes:
            t = dim_nodes(x)
            total = total + t[0]
            row = max(row, t[1])
            col = col + t[2]
        return (1+total, 1+row, col)
    elif isinstance(n, Printnl):
        t = dim_nodes(n.nodes[0])
        return (1+t[0], 1+t[1], t[2])
    elif isinstance(n, Assign):
        t0 = dim_nodes(n.nodes[0])
        t1 = dim_nodes(n.expr)
        return ((1+t0[0]+t1[0]), 1+max(t0[1], t1[1]), t0[2]+t1[2])
    elif isinstance(n, AssName):
        return (1, 1, 1)
    elif isinstance(n, Discard):
        t = dim_nodes(n.expr)
        return ((1+t[0]), 1+t[1], t[2])
    elif isinstance(n, Const):
        return (1, 1, 1)
    elif isinstance(n, Name):
        return (1, 1, 1)
    elif isinstance(n, Add):
        t0 = dim_nodes(n.left)
        t1 = dim_nodes(n.right)
        return (1+t0[0]+t1[0], 1+max(t0[1], t1[1]), t0[2]+t1[2])
    elif isinstance(n, UnarySub):
        t = dim_nodes(n.expr)
        return (1+t[0], 1+t[1], t[2])
    elif isinstance(n, CallFunc):
        t = dim_nodes(n.node)
        return (1+t[0], 1+t[1], t[2])
    else:
        raise Exception('Error in dim_nodes: unrecognized AST node')

def unparse(n):
    raise Exception('Not yet implemented')

def del_dim(A, B):
    dimA = dim_nodes(A);
    dimB = dim_nodes(B);
    return ((dimA[0]-dimB[0]), (dimA[1]-dimB[1]), (dimA[2]-dimB[2]))

def drawast(n, row=0, col=0, output=None):

    if output is None:
        dim = dim_nodes(n);
        output = [["" for i in range(dim[2])] for j in range(dim[1])]
    
    if isinstance(n, Module):
        output[row][col] = "Module"
        return ["Module"]+drawast(n.node, row+1, col, output)
    elif isinstance(n, Stmt):
        output[row][col] = "Stmt"
        cols = 0
        lsttmp = list()
        for x in n.nodes:
            lsttmp = lsttmp+[drawast(x, row+1, col+cols, output)]
            dim = dim_nodes(x)
            cols = cols + dim[2]
        return ["Stmt"]+lsttmp
    elif isinstance(n, Printnl):
        output[row][col] = "Printnl"
        return ["Printnl"]+drawast(n.nodes[0], row+1, col, output)
    elif isinstance(n, Assign):
        output[row][col] = "Assign"
        dim = dim_nodes(n.nodes[0]);
        return ["Assign"]+[drawast(n.nodes[0], row+1, col, output)]+[drawast(n.expr, row+1, col+dim[2], output)]
    elif isinstance(n, AssName):
        output[row][col] = "AssName"
        return ["AssName"]
    elif isinstance(n, Discard):
        output[row][col] = "Discard"
        return ["Discard"]+drawast(n.expr, row+1, col, output)
    elif isinstance(n, Const):
        output[row][col] = "Const"
        return ["Const"]
    elif isinstance(n, Name):
        output[row][col] = "Name"
        return ["Name"]
    elif isinstance(n, Add):
        output[row][col] = "Add"
        dim = dim_nodes(n.left);
        return ["Add"]+[drawast(n.left, row+1, col, output)]+[drawast(n.right, row+1, col+dim[2], output)]
    elif isinstance(n, UnarySub):
        output[row][col] = "UnarySub"
        return ["UnarySub"]+drawast(n.expr, row+1, col, output)
    elif isinstance(n, CallFunc):
        output[row][col] = "CallFunc"
        return ["CallFunc"]+drawast(n.node, row+1, col, output)
    else:
        raise Exception('Error in drawast: unrecognized AST node')

def pt(tree, offset=0, term=0):
    
    for i in range(len(tree)):
        if isinstance(tree[i], list):
            if(i < (len(tree) - 1)):
                pt(tree[i], offset+1, term+0)
            else:
                pt(tree[i], offset+1, term+1)
        else:
            #Write Offset
            for j in range(offset):
                sys.stderr.write((str(offset-term)).rjust(15))
            
            #Write Node
            if(i == 0 and offset != 0):
                #First Node
                line = ""
                for j in range(15-len(str(tree[i]))):
                    line = line+"-"
                sys.stderr.write((line+str(tree[i])).rjust(15)+"\n")
            else:
                sys.stderr.write(str(tree[i]).rjust(15)+"\n")

            #Write Offset
            for j in range(offset):
                sys.stderr.write((str(offset-term)).rjust(15))

            #Write Seperator
            if(i < (len(tree) - 1)):
                #Last Node
                sys.stderr.write("|".rjust(15)+"\n")
            else:
                sys.stderr.write(" ".rjust(15)+"\n")

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

    # Measure Tree
    num1 = dim_nodes(ast)
    sys.stderr.write(str(argv[0]) + ": dim_nodes(ast) = " + str(num1) + "\n")
    
    # Draw Tree
    pt(drawast(ast, 0, 0))
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
