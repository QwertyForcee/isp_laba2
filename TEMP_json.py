from json_serializer import JsonSerializer

jser = JsonSerializer()

bigVariable = 55_192_217

class bigA:
    a = {4:'3333',41:'im tired'}

    @classmethod
    def stupied_func_name():
        print('stupied output')
        
    @classmethod
    def biVar():
        print(bigVariable)

    

data = jser.dumps(bigA)
obj = jser.loads(data)
print(obj.a)
print(obj.stupied_func_name)
print(obj.biVar)


