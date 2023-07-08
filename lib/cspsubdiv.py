#!/usr/bin/env python
from bezmisc import *
from ffgeom import *


def maxdist(points):
    p0x, p0y = points[0]
    p1x, p1y = points[1]
    p2x, p2y = points[2]
    p3x, p3y = points[3]

    p0 = Point(p0x, p0y)
    p1 = Point(p1x, p1y)
    p2 = Point(p2x, p2y)
    p3 = Point(p3x, p3y)

    s1 = Segment(p0, p3)
    return max(s1.distanceToPoint(p1), s1.distanceToPoint(p2))


def cspsubdiv(csp, flat):
    for sp in csp:
        subdiv(sp, flat)


def subdiv_recursive(sp, flat, i=1):
    p0 = sp[i - 1][1]
    p1 = sp[i - 1][2]
    p2 = sp[i][0]
    p3 = sp[i][1]

    b = (p0, p1, p2, p3)
    m = maxdist(b)
    if m <= flat:
        try:
            subdiv(sp, flat, i + 1)
        except IndexError:
            pass
    else:
        one, two = beziersplitatt(b, 0.5)
        sp[i - 1][2] = one[1]
        sp[i][0] = two[2]
        p = [one[2], one[3], two[1]]
        sp[i:1] = [p]
        subdiv(sp, flat, i)


def subdiv(sp, flat):
    # This is a non-recursive version of the above function
    # and avoids a `RecursionError: maximum recursion depth exceeded` error
    stack = [(1, len(sp))]
    while stack:
        i, end = stack.pop()
        while i < end:
            p0 = sp[i - 1][1]
            p1 = sp[i - 1][2]
            p2 = sp[i][0]
            p3 = sp[i][1]

            b = (p0, p1, p2, p3)
            m = maxdist(b)
            if m > flat:
                one, two = beziersplitatt(b, 0.5)
                sp[i - 1][2] = one[1]
                sp[i][0] = two[2]
                p = [one[2], one[3], two[1]]
                sp.insert(i, p)
                end += 1
            i += 1
        stack.extend([(i, end) for i in range(i, end)])
