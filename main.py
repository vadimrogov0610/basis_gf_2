from Basis import Basis


def linear_to_int(s: str):
    return sum(map(lambda t: 1 << t, [int(u[1:]) for u in s.split(' + ')]))


def int_to_linear(j: int):
    ans = []
    count = 0
    while j:
        if j & 1:
            ans.append(f'x{count}')
        j >>= 1
        count += 1
    return ' + '.join(reversed(ans))


r1 = 'x4 + x2 + x0'
r2 = 'x3 + x2'
r3 = 'x3 + x2 + x0'
r4 = 'x4 + x2'

# __init__ makes gauss method (optimized for Python)
b = Basis([linear_to_int(u) for u in [r1, r2, r3, r4]])
for i in b:
    print(int_to_linear(i))
# x4 + x2
# x3 + x2
# x0

s1 = 'x5 + x4 + x1'
s2 = 'x5 + x1'
s3 = 'x2'
c = Basis([linear_to_int(u) for u in [s1, s2, s3]])
for i in c:
    print(int_to_linear(i))
# x5 + x1
# x4
# x2

# Basis of sum of linear spaces
summa = b + c
for i in summa:
    print(int_to_linear(i))
# x5 + x1
# x4
# x3 + x2
# x2
# x0

# Basis of intersection of linear spaces
intersection = b * c
for i in intersection:
    print(int_to_linear(i))
# x4 + x2

# Adding new element
new = linear_to_int('x3 + x1')
print(b.belongs(new))
# False
b.add(new)
for i in b:
    print(int_to_linear(i))
# x4 + x2
# x3 + x2
# x2 + x1
# x0

# Making reverse gauss move
r1 = 'x3 + x2 + x1 + x0'
r2 = 'x2 + x1 + x0'
r3 = 'x1 + x0'
r4 = 'x0'
c = Basis([linear_to_int(u) for u in [r1, r2, r3, r4]])
c.reverse_gauss()
for i in c:
    print(int_to_linear(i))
# x3
# x2
# x1
# x0
