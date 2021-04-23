from toml_serializer import TomlSerializer

o = {'head':{'a':"I'm a string",'b':["I'm","a","string"],'c':1212,'d':True}}

f = open('somedata.toml','w')
TomlSerializer().dump(o,f)
f.close()

