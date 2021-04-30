from json_serializer import JsonSerializer

jser = JsonSerializer()

def teest():
    print('123')
    return '321'

obj = jser.load(open('clear.json'))

print('obj.a',obj.a)

print('obj.b',obj.b)
print('obj.x',obj.x)
print('obj.InsideClass.insidevalue',obj.InsideClass.insidevalue)
obj.hate()
print(obj.square(6))

