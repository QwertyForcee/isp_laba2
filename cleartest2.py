from json_serializer import JsonSerializer

jser = JsonSerializer()

def teest():
    print('123')
    return '321'

obj = jser.load(open('clear.json'))
"""
print(obj.__globals__)
print(obj)

print(obj.__globals__)
"""

obj=obj()

print(obj.a)
print(obj.b)
print(obj.x)
print(obj.InsideClass.insidevalue)
print(obj.hate())
