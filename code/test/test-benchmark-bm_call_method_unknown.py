#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-benchmark-bm_call_methode_unknown.py
# Test Case
# Subset: benchmark
# Type: Student
# Tesing: benchmark
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

class Foo:

    def foo(a, b, c):
        # 20 calls
        b.bar(a, c)
        b.bar(c, a)
        c.bar(a, b)
        c.bar(b, a)
        b.bar(a, c)
        b.bar(c, a)
        c.bar(a, b)
        c.bar(b, a)
        b.bar(a, c)
        b.bar(c, a)
        c.bar(a, b)
        c.bar(b, a)
        b.bar(a, c)
        b.bar(c, a)
        c.bar(a, b)
        c.bar(b, a)
        b.bar(a, c)
        b.bar(c, a)
        c.bar(a, b)
        c.bar(b, a)

    def bar(a, b, c):
        # 20 calls
        b.baz(a, c)
        b.baz(c, a)
        c.baz(a, b)
        c.baz(b, a)
        b.baz(a, c)
        b.baz(c, a)
        c.baz(a, b)
        c.baz(b, a)
        b.baz(a, c)
        b.baz(c, a)
        c.baz(a, b)
        c.baz(b, a)
        b.baz(a, c)
        b.baz(c, a)
        c.baz(a, b)
        c.baz(b, a)
        b.baz(a, c)
        b.baz(c, a)
        c.baz(a, b)
        c.baz(b, a)

    def baz(a, b, c):
        # 20 calls
        b.quux(a, c)
        b.quux(c, a)
        c.quux(a, b)
        c.quux(b, a)
        b.quux(a, c)
        b.quux(c, a)
        c.quux(a, b)
        c.quux(b, a)
        b.quux(a, c)
        b.quux(c, a)
        c.quux(a, b)
        c.quux(b, a)
        b.quux(a, c)
        b.quux(c, a)
        c.quux(a, b)
        c.quux(b, a)
        b.quux(a, c)
        b.quux(c, a)
        c.quux(a, b)
        c.quux(b, a)

    def quux(a, b, c):
        # 20 calls
        b.qux(a, c)
        b.qux(c, a)
        c.qux(a, b)
        c.qux(b, a)
        b.qux(a, c)
        b.qux(c, a)
        c.qux(a, b)
        c.qux(b, a)
        b.qux(a, c)
        b.qux(c, a)
        c.qux(a, b)
        c.qux(b, a)
        b.qux(a, c)
        b.qux(c, a)
        c.qux(a, b)
        c.qux(b, a)
        b.qux(a, c)
        b.qux(c, a)
        c.qux(a, b)
        c.qux(b, a)

    def qux(a, b, c):
        return 0


class Bar:

    def foo(a, b, c):
        # 20 calls
        b.bar(a, c)
        b.bar(c, a)
        c.bar(a, b)
        c.bar(b, a)
        b.bar(a, c)
        b.bar(c, a)
        c.bar(a, b)
        c.bar(b, a)
        b.bar(a, c)
        b.bar(c, a)
        c.bar(a, b)
        c.bar(b, a)
        b.bar(a, c)
        b.bar(c, a)
        c.bar(a, b)
        c.bar(b, a)
        b.bar(a, c)
        b.bar(c, a)
        c.bar(a, b)
        c.bar(b, a)

    def bar(a, b, c):
        # 20 calls
        b.baz(a, c)
        b.baz(c, a)
        c.baz(a, b)
        c.baz(b, a)
        b.baz(a, c)
        b.baz(c, a)
        c.baz(a, b)
        c.baz(b, a)
        b.baz(a, c)
        b.baz(c, a)
        c.baz(a, b)
        c.baz(b, a)
        b.baz(a, c)
        b.baz(c, a)
        c.baz(a, b)
        c.baz(b, a)
        b.baz(a, c)
        b.baz(c, a)
        c.baz(a, b)
        c.baz(b, a)

    def baz(a, b, c):
        # 20 calls
        b.quux(a, c)
        b.quux(c, a)
        c.quux(a, b)
        c.quux(b, a)
        b.quux(a, c)
        b.quux(c, a)
        c.quux(a, b)
        c.quux(b, a)
        b.quux(a, c)
        b.quux(c, a)
        c.quux(a, b)
        c.quux(b, a)
        b.quux(a, c)
        b.quux(c, a)
        c.quux(a, b)
        c.quux(b, a)
        b.quux(a, c)
        b.quux(c, a)
        c.quux(a, b)
        c.quux(b, a)

    def quux(a, b, c):
        # 20 calls
        b.qux(a, c)
        b.qux(c, a)
        c.qux(a, b)
        c.qux(b, a)
        b.qux(a, c)
        b.qux(c, a)
        c.qux(a, b)
        c.qux(b, a)
        b.qux(a, c)
        b.qux(c, a)
        c.qux(a, b)
        c.qux(b, a)
        b.qux(a, c)
        b.qux(c, a)
        c.qux(a, b)
        c.qux(b, a)
        b.qux(a, c)
        b.qux(c, a)
        c.qux(a, b)
        c.qux(b, a)

    def qux(a, b, c):
        return 0


class Baz:

    def foo(a, b, c):
        # 20 calls
        b.bar(a, c)
        b.bar(c, a)
        c.bar(a, b)
        c.bar(b, a)
        b.bar(a, c)
        b.bar(c, a)
        c.bar(a, b)
        c.bar(b, a)
        b.bar(a, c)
        b.bar(c, a)
        c.bar(a, b)
        c.bar(b, a)
        b.bar(a, c)
        b.bar(c, a)
        c.bar(a, b)
        c.bar(b, a)
        b.bar(a, c)
        b.bar(c, a)
        c.bar(a, b)
        c.bar(b, a)

    def bar(a, b, c):
        # 20 calls
        b.baz(a, c)
        b.baz(c, a)
        c.baz(a, b)
        c.baz(b, a)
        b.baz(a, c)
        b.baz(c, a)
        c.baz(a, b)
        c.baz(b, a)
        b.baz(a, c)
        b.baz(c, a)
        c.baz(a, b)
        c.baz(b, a)
        b.baz(a, c)
        b.baz(c, a)
        c.baz(a, b)
        c.baz(b, a)
        b.baz(a, c)
        b.baz(c, a)
        c.baz(a, b)
        c.baz(b, a)

    def baz(a, b, c):
        # 20 calls
        b.quux(a, c)
        b.quux(c, a)
        c.quux(a, b)
        c.quux(b, a)
        b.quux(a, c)
        b.quux(c, a)
        c.quux(a, b)
        c.quux(b, a)
        b.quux(a, c)
        b.quux(c, a)
        c.quux(a, b)
        c.quux(b, a)
        b.quux(a, c)
        b.quux(c, a)
        c.quux(a, b)
        c.quux(b, a)
        b.quux(a, c)
        b.quux(c, a)
        c.quux(a, b)
        c.quux(b, a)

    def quux(a, b, c):
        # 20 calls
        b.qux(a, c)
        b.qux(c, a)
        c.qux(a, b)
        c.qux(b, a)
        b.qux(a, c)
        b.qux(c, a)
        c.qux(a, b)
        c.qux(b, a)
        b.qux(a, c)
        b.qux(c, a)
        c.qux(a, b)
        c.qux(b, a)
        b.qux(a, c)
        b.qux(c, a)
        c.qux(a, b)
        c.qux(b, a)
        b.qux(a, c)
        b.qux(c, a)
        c.qux(a, b)
        c.qux(b, a)

    def qux(a, b, c):
        return 0


def test_calls(iterations):
    a = Foo()
    b = Bar()
    c = Baz()
    i = 0
    while i != iterations:
        i = i + 1
        # 18 calls
        a.foo(b, c)
        b.foo(c, a)
        c.foo(a, b)
        a.foo(b, c)
        b.foo(c, a)
        c.foo(a, b)
        a.foo(b, c)
        b.foo(c, a)
        c.foo(a, b)
        a.foo(b, c)
        b.foo(c, a)
        c.foo(a, b)
        a.foo(b, c)
        b.foo(c, a)
        c.foo(a, b)
        a.foo(b, c)
        b.foo(c, a)
        c.foo(a, b)
    return 0

test_calls(1)
