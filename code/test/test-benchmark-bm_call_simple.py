#!/usr/bin/python

# CU CS5525
# Fall 2012
# Python Compiler
#
# test-benchmark-bm_call_simple.py
# Test Case
# Subset: benchmark
# Type: Student
# Tesing: benchmark
#
# Repository:
#    https://github.com/asayler/CU-CS5525-PythonCompiler
#
# By : Google

def foo(a, b, c, d):
    # 20 calls
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)
    bar(a, b, c)


def bar(a, b, c):
    # 20 calls
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)
    baz(a, b)


def baz(a, b):
    # 20 calls
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)
    quux(a)


def quux(a):
    # 20 calls
    qux()
    qux()
    qux()
    qux()
    qux()
    qux()
    qux()
    qux()
    qux()
    qux()
    qux()
    qux()
    qux()
    qux()
    qux()
    qux()
    qux()
    qux()
    qux()
    qux()


def qux():
    return 0


def test_calls(iterations):
    i = 0
    while i != iterations:
        i = i + 1
        # 20 calls
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
        foo(1, 2, 3, 4)
    return 0

test_calls(1)
