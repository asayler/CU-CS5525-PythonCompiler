# CU CS5525
# Fall 2012
# Python Compiler
#
# explicate.py
# Visitor Functions to Explicate AST
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

import sys

# Data Types
from pyast import *
from set_visitor import *

from unitcopy import CopyVisitor

# Helper Types
from vis import Visitor
from functionwrappers import *
from utilities import generate_name

class StringFindVisitor(SetVisitor):
    def visitString(self, n):
        location = '.L' + generate_name('str')
        n.location = location
        return set([(location, n.string)])
