from yaml_serializer import YamlSerializer

res = YamlSerializer().load(open('useglob.yml'))


iitp = YamlSerializer().load(open('iitpclass.yml'))
#iitp = iitp()
"""
s1 = iitp.Student()
s1.name = "Maxim Bystrov"
s1.av_score = 5

s2 = iitp.Student()
s2.name = "Prostoi Ivan"
s2.av_score = 7
iitp.students=[s1,s2]
"""
print(iitp)
data = YamlSerializer().dumps(iitp)
#print(data)
iitp = YamlSerializer().loads(data) 
iitp = iitp()
print(iitp.Student.name,iitp.Student.av_score)
print(iitp.students)
iitp.expel()
print(iitp.students)
iitp.introduction()

print(res())


