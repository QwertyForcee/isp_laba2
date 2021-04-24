from serializer import Serializer

globalglobal=100
class Noname:
    a = 5
    b = 12
    myy = lambda x:'lambda return value'

    def ab(self):
        return self.a*self.b

    def pr_global(self):
        print(globalglobal)


data = Serializer().to_valid_dict(Noname())
myclass = Serializer().to_valid_obj(data)
print(myclass)
myclass.pr_global()


#data = Serializer().to_valid_dict(square)
#myfunction = Serializer().to_valid_obj(data)
#print(myfunction())
#print(square.__name__)
#print(square.__globals__)
