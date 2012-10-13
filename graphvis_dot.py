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

import sys, uuid

nodecnt = 0

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
