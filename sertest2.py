from serializer import Serializer
gl = 888

class Cat:
    cuttie = 1000
    def Meow(self):
        print("Meow")

    def Murr(self):
        print("Murr")

    def pr_gl(self):
        print(gl)

    class A:
        value = 8341


data = Serializer().to_valid_dict(Cat())

mycat = Serializer().to_valid_obj(data)
print(mycat)
print(mycat.cuttie)
mycat.Meow()
mycat.Murr()
print('before')
mycat.pr_gl()
print('after')
gl = 121212
mycat.pr_gl()

val = mycat.A()
print('Cat A', val.value)



def func123():
    print(123)