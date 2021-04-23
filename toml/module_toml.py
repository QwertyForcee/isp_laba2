from toml_serializer import TomlSerializer

o = {'head':{'a':"I'm a string",'b':["I'm","a","string"],'c':1212,'d':True}}


data = TomlSerializer().dumps(o)

obj = TomlSerializer().loads(data)
print(type(obj))
print(obj)

