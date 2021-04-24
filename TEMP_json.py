from json_serializer import JsonSerializer

jser = JsonSerializer()

bigVariable = 55_192_217

class bigA:
    a = {4:'3333',41:'im tired'}

    def stupied_func_name(self):
        print('stupied output')
        
    def biVar(self):
        print(bigVariable)

myA = bigA()
myA.biVar()

data = jser.dumps(bigA)
obj1 = jser.loads(data)
obj = obj1()
print(obj.a)
print(obj.stupied_func_name())
print(obj.biVar())


