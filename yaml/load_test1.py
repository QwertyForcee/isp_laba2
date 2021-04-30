from yaml_serializer import YamlSerializer

res = YamlSerializer().load(open('useglob.yml'))
"""
iitp = YamlSerializer().load(open('iitpclass.yml'))
print(iitp)
iitp = iitp()
iitp.students=['Maxim Bystrov','123 123','321 321']
print(iitp.students)
print(iitp.expel())
print(iitp.students)
"""
print(res)
res()
