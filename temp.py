class Cat:
    def meow():
        print('meeow')
    def murr():
        print('murr')

b=123
def func():
    a=5
    c=12
    d=1

    print(a+b+c+d)

print('funcname',func.__name__)

#print(func.__globals__)
b=33
code_obj = func.__code__
#Attributes of code object
#print(dir(code_obj))
#The variable Names
obj_globals = dict()
for c in code_obj.co_names:
    if c in globals():
        obj_globals[c]=globals()[c]

#print(obj_globals)
flocals = dict()
for i in range(code_obj.co_nlocals):
    flocals[code_obj.co_varnames[i]]=code_obj.co_consts[i+1]
print(code_obj.co_consts)
print(code_obj.co_varnames)
print(code_obj.co_names)
#print(flocals)
#exec(code_obj)