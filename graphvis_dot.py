# Andy Sayler
# Fall 2012
# CU CS5525
# Python Compiler
# Functions to produce an GraphViz "dot" input file
#
# In conjunction with:
#    Michael (Mike) Vitousek
#       https://github.com/mvitousek/python-compiler-mmv
#    Anne Gatchell
#       https://github.com/halloannielala/compiler-5525

import sys

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

    def linePair(self, parent, child):
        pid = self.qt + str(id(parent)) + self.qt
        cid = self.qt + str(id(child))  + self.qt
        return [(pid + self.arrow + cid + self.sc)]

    def lineLabel(self, n, label):
        nid = self.qt + str(id(n)) + self.qt        
        return [(nid + " " +
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
