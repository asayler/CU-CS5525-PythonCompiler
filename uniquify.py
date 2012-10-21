# CU CS5525
# Fall 2012
# Python Compiler
#
# uniquify.py
# Visitor Funstions to Uniquify AST
#
# Adopted from code by Jeremy Siek, Fall 2012
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
from compiler.ast import *
from monoast import *

from unitcopy import CopyVisitor

# Helper Types
from vis import Visitor
from functionwrappers import *
from utilities import generate_name

class UniquifyVisitor(CopyVisitor):
	def __init__(self):
		super(UniquifyVisitor, self).__init__()

	