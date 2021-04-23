from toml_serializer import TomlSerializer

o = {'a':"I'm a string",'b':["I'm","a","string"],'c':1212}

print(TomlSerializer().dumps(o))


