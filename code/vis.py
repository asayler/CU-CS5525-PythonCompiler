# CU CS5525
# Fall 2012
# GSV Python Compiler
#
# vis.py
# Generic Visitor Implmentation
#
# Adopted from code by Jeremy Siek, Fall 2012
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

debug = False

class Visitor(object):
    def __init__(self):
        self.node = None
        self._cache = {}

    def default(self, node, *args):
        raise Exception('no visit method for type %s in %s for %s' \
                        % (node.__class__, self.__class__, repr(node)))

    def valid(self, node, stage):
        return filter(lambda x: x == stage, node.valid_stages)

    def dispatch(self, node, *args):
        if debug:
            print repr(self.__class__) + 'dispatching for ' + repr(node.__class__)
            print '   ' + repr(node) + ' in ' \
                  + self.__class__.__name__
        self.node = node
        klass = node.__class__
        meth = self._cache.get(klass, None)
        if meth is None:
            className = klass.__name__
            meth = getattr(self.visitor, 'visit' + className, self.default)
            self._cache[klass] = meth
        ret = meth(node, *args)
        if debug:
            print 'finished with ' + repr(node.__class__)
        return ret

    def preorder(self, tree, *args):
        """Do preorder walk of tree using visitor"""
        self.visitor = self
        return self.dispatch(tree, *args)



