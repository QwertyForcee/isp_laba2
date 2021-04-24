from json_serializer import JsonSerializer
glob = 222444


def privet():
    print(glob)


#JsonSerializer().dump(privet,open('example.json','w'))
ooo = JsonSerializer().load(open('example.json','r'))

ooo()