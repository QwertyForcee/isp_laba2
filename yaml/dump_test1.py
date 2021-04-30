from yaml_serializer import YamlSerializer

pi = 3.14159265359
def use_glob():
    print(pi)

class Iitp:
    students = list()
    def expel(self):
        self.students = list()


YamlSerializer().dump(Iitp,open('iitpclass.yml','w'))

YamlSerializer().dump(use_glob,open('useglob.yml','w'))