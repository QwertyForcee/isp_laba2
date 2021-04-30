from yaml_serializer import YamlSerializer

#res = YamlSerializer().load(open('useglob.yml'))


iitp = YamlSerializer().load(open('iitpclass.yml'))
iitp = iitp()

s1 = iitp.Student()
s1.name = "Maxim Bystrov"
s1.av_score = 5

s2 = iitp.Student()
s2.name = "Ivan Ivanovich"
s2.av_score = 7

iitp.students=[s1,s2]
print(iitp.students)
iitp.expel()
print(iitp.students)
iitp.introduction()

#print(res)
#res()
