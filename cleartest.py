from json_serializer import JsonSerializer

jser = JsonSerializer()
glob = "i'm a global variable"
global_hate = "i hate class method's  serialization :)))"

class Simple:
    a=5
    b=787
    x=[9,8,7,6,5,4,21]
    class InsideClass:
        insidevalue="inside value"

    def hate(self):
        return global_hate

def say():
    print('privet))')

jser.dump(Simple,open('clear.json','w'))