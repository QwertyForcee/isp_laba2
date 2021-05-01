from json_serializer import JsonSerializer
from toml_serializer import TomlSerializer

jser = JsonSerializer()
toml = TomlSerializer()
glob = "i'm a global variable"
global_hate = "i hate class method's  serialization :)))"




a= 213
class Simple:
    a=5
    b=787
    x=[9,8,7,6,5,4,21]

    square=lambda slf,x: x**2

    class InsideClass:
        insidevalue="inside value"

    def hate(self):
        print(global_hate)
    

a = {(123,321):'123'}

s = Simple()



def say():
    print(glob)

jser.dump(Simple(),open('clear.json','w'))
toml.dump(Simple(),open('clear1.toml','w'))