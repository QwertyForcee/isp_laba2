from yaml_serializer import YamlSerializer

a= {'1':2114,'2':'1212','3':False,'4':['helo','froma','liste'],'5':{'here':'is','a':'dictionary'}}

class Yamla():
    about = "god knows what it is"
    somedata = [9,8,7,6,5,4,3,2,1,0]

#YamlSerializer().dump(Yamla,open('yamla.yml','w'))
res = YamlSerializer().dumps(a)
print(res)
s = res.split('\n')
print(s)
