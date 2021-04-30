from yaml_serializer import YamlSerializer

pi = 3.14159265359
def use_glob():
    return pi

class Iitp:
    class Student:
        name = "noname"
        av_score = 4

    def introduction(self):
        print("The best speciality in the world.")

    students = list()

    def expel(self):
        self.students = list()

iitp = Iitp()
s1 = iitp.Student()
s1.name = "Maxim Bystrov"
s1.av_score = 5

s2 = iitp.Student()
s2.name = "Prostoi Ivan"
s2.av_score = 7

iitp.students=[s1,s2]

YamlSerializer().dump(iitp,open('iitpclass.yml','w'))

YamlSerializer().dump(use_glob,open('useglob.yml','w'))