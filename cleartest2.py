from json_serializer import JsonSerializer

jser = JsonSerializer()

obj = jser.load(open('clear.json'))
print(obj())


"""
print(obj.a)
print(obj.x)
print(obj.InsideClass.insidevalue)
print(obj.hate())
"""