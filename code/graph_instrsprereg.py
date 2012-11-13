# Andy Sayler
# Fall 2012
# CU CS5525
# Python Compiler
# Visitor to graph an instruction ast
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

import sys
import compiler

from x86ast import *

from graphvis_dot import Graphvis_dot

from vis import Visitor

class Graph_instrspreast():
    
    def writeGraph(self, ast, filepath):
        lines = self.preorder(ast)
        Graphvis_dot().drawGraph(lines, filepath)
