import types
import inspect
from fortest import MySerializer

class Cat:
    def meow():
        print('meeow')
    def murr():
        print('murr')

c = Cat()
some_global = 9999
def f():
    print('some',some_global)

obj = f.__code__
f = MySerializer().func_to_valid(f)
some_global=12
f()
