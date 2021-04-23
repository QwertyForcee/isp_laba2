from serializer import Serializer

class Cat:
    cuttie = 1000
    def Meow(self):
        print("Meow")
    def Murr(self):
        print("Murr")

print(Cat.__bases__)

data = Serializer().to_valid_dict(Cat())

mycat = Serializer().to_valid_obj(data)
print(mycat)
mycat.Meow()
mycat.Murr()
print(mycat.cuttie)

