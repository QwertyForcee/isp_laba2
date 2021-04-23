import types

def square(x):
    print(x**2)
    return x**2

cobj = square.__code__
data = list()
custom=[o for o in cobj.__class__.__dict__.items() if not o[0].startswith('__')]
for c in custom:
    data.append(c[0])
print(data)
#print(cobj.__class__.__dict__.items())
