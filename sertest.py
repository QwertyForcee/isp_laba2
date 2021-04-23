from serializer import Serializer

globalglobal=100
class Noname:
    a = 5
    b = 12
    myy = lambda x:'lambda return value'

    def ab(self):
        return self.a*self.b

"""
data = Serializer().to_valid_dict(Noname)
myclass = Serializer().to_valid_obj(data)
print(myclass)
no = myclass()
print(no.myy())
"""
from pydoc import locate

print(locate("object"))
#data = Serializer().to_valid_dict(square)
#myfunction = Serializer().to_valid_obj(data)
#print(myfunction())
#print(square.__name__)
#print(square.__globals__)