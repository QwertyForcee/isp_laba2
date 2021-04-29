from yaml_serializer import YamlSerializer

res = YamlSerializer().load(open('useglob.yml'))

print(res)
res()
