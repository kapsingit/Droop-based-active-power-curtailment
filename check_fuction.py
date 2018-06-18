
global a
a = 2
global c
c = 3

def myfunc(d):
    global c
    e = a*2
    b = 3
    a = 3
    c = 4
    return b

d = myfunc(2)
