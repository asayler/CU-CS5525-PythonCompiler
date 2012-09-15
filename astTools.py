# Andy Sayler
# Fal 2012
# CU CS5525
# Python AST Tools
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

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
