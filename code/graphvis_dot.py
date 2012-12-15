# CU CS5525
# Fall 2012
# GSV Python Compiler
#
# graphvis_dot.py
# Functions to produce an GraphViz "dot" input file
#
# Repository:
#    https://github.com/asayler/CU-CS5525-PythonCompiler
#
# By :
#    Anne Gatchell
#       http://annegatchell.com/
#    Andrew (Andy) Sayler
#       http://www.andysayler.com
#    Michael (Mike) Vitousek
#       http://csel.cs.colorado.edu/~mivi2269/
#
# Copyright (c) 2012 by Anne Gatchell, Andy Sayler, and Mike Vitousek
#
# This file is part of the GSV CS5525 Fall 2012 Python Compiler.
#
#    The GSV CS5525 Fall 2012 Python Compiler is free software: you
#    can redistribute it and/or modify it under the terms of the GNU
#    General Public License as published by the Free Software
#    Foundation, either version 3 of the License, or (at your option)
#    any later version.
#
#    The GSV CS5525 Fall 2012 Python Compiler is distributed in the
#    hope that it will be useful, but WITHOUT ANY WARRANTY; without
#    even the implied warranty of MERCHANTABILITY or FITNESS FOR A
#    PARTICULAR PURPOSE.  See the GNU General Public License for more
#    details.
#
#    You should have received a copy of the GNU General Public License
#    along with the GSV CS5525 Fall 2012 Python Compiler.  If not, see
#    <http://www.gnu.org/licenses/>.

import sys, uuid

class Graphvis_dot():

    digraphOpen = "digraph G {"
    digraphClose = "}"
    attrOpen = "["
    attrClose = "]"
    attrLabel = "label="
    arrow = " -> "
    qt = '\"'
    sc = ';'
    nl = '\n'
    tb = '\t'
    nltb = nl + tb

    def uniqueid(self, node):
        return uuid.uuid4()

    def linePair(self, pid, cid):
        pid = self.qt + str(pid) + self.qt
        cid = self.qt + str(cid)  + self.qt
        return [(pid + self.arrow + cid + self.sc)]

    def lineLabel(self, myid, label):
        myid = self.qt + str(myid) + self.qt        
        return [(myid + " " +
                 self.attrOpen + self.attrLabel +
                 self.qt + label + self.qt +
                 self.attrClose + self.sc)]

    def drawGraph(self, lines, filepath):
        graph = (self.digraphOpen + self.nltb +
                 self.nltb.join(lines) +
                 self.nl + self.digraphClose)
        outputfile = open(filepath, 'w+')
        outputfile.write(graph + self.nl)
        outputfile.close()
