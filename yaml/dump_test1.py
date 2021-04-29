from yaml_serializer import YamlSerializer

pi = 3.14159265359
def use_glob():
    print(pi)

YamlSerializer().dump(use_glob,open('useglob.yml','w'))