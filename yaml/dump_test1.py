from yaml_serializer import YamlSerializer

pi = 3.14159265359
def use_glob():
    print(pi)

class Iitp:
    class Student:
        name = "noname"
        av_score = 4

    def introduction(self):
        print("The best speciality in the world.")

    students = list()

    def expel(self):
        self.students = list()


YamlSerializer().dump(Iitp,open('iitpclass.yml','w'))

YamlSerializer().dump(use_glob,open('useglob.yml','w'))