import math

S = lambda c: (lambda i: (i, i+1) if i < 51 else (51, 9999))(ord(c) - 65)

def d(s):
    lo, hi = 0.0, 19683.0
    for c in s:
        a, b = S(c)
        w = hi - lo
        lo = lo + w * (a / 9999)
        hi = lo + w * ((b - a) / 9999)
    return lo, hi

f = lambda x: int((x - math.floor(x)) * 1e13 + 0.5)

word = "SATOR"
lo, hi = d(word)
print("lo:", lo)
print("hi:", hi)
print("f(lo):", f(lo))
print("f(hi):", f(hi))
