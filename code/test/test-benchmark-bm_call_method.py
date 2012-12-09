#!/usr/bin/env python


class Foo:
    def foo(self, a, b, c, d):
        # 20 calls
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)
        self.bar(a, b, c)

    def bar(self, a, b, c):
        # 20 calls
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)
        self.baz(a, b)

    def baz(self, a, b):
        # 20 calls
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)
        self.quux(a)

    def quux(self, a):
        # 20 calls
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()
        self.qux()

    def qux(self):
        return 0


def test_calls(iterations):
    f = Foo()
    i = 0
    while i != iterations:
        i = i + 1
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
        f.foo(1, 2, 3, 4)
    return 0

test_calls(1)
