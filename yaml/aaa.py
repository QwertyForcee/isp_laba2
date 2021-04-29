from yaml_serializer import YamlSerializer

data = open('yamla.yml').read()

res = YamlSerializer().loads(data)
print(res)
temp = 123

