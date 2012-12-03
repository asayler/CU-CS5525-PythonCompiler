# CU CS5525
# Fall 2012
# Python Compiler
#
# propagate.py
# Visitor Functions to Remove Direct Assignments fro AST
#
# Repository:
#    https://github.com/asayler/CU-CS5525-PythonCompiler
#
# By :
#    Anne Gatchell
#       http://annegatchell.com/
#    Andy Sayler
#       http://www.andysayler.com
#    Michael (Mike) Vitousek
#       http://csel.cs.colorado.edu/~mivi2269/

# Helper Tools
from utilities import generate_name, make_assign
from copy_visitor import CopyVisitor

from functionwrappers import *

# Data Types
from pyast import *

class PropagateVisitor(CopyVisitor):
    
    def __init__(self):
        super(PropagateVisitor,self).__init__()

    def preorder(self, tree):
        self.names = {}
        return super(PropagateVisitor, self).preorder(tree)
