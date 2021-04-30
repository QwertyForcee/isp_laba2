class A:
    foo=123
    bar=500

class B:
    pass

a=A()
a.foo =1
print(a.__dict__)
#a=dict()
#for x in A().__dict__.items():
#    a[x[0]] = str(x[1])


