def countto_iter(x, limit):
    print x
    return (x if x == limit else countto(x + 1, limit))

def countto(limit):
    return countto_iter(0, limit)

countto(12)
countto(input())
