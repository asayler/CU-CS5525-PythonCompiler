# CU CS5525
# Fall 2012
# Python Compiler
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
#    Andy Sayler
#       http://www.andysayler.com
#    Michael (Mike) Vitousek
#       http://csel.cs.colorado.edu/~mivi2269/

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
