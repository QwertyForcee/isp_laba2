from yaml_serializer import YamlSerializer
import re

a= {'1':2114,'2':'1212','3':False,'4':['helo','froma','liste'],'5':{'here':'is','a':'dicti onary'}}

class Yamla():
    about = "god knows what it is"
    somedata = {'1':'poka bez listov','2':'XD'}
    #somedata = [9,8,7,6,5,4,3,2,1,0]

#YamlSerializer().dump(Yamla,open('yamla.yml','w'))
res = YamlSerializer().dumps(a)
s = res.split('\n')
print(s)
data = dict()
for string in s:
    temp =re.findall(r"(\w+): (\w+)",string)
    if len(temp)>0:
        value = temp[0][1]
        try:
            res = int(value)
        except:
            res = value
            if value == 'true' or value == 'True':
                res = True
            elif value == 'false' or value == 'False':
                res = False
        data[temp[0][0]] = res         
        continue
        #print(temp)
    temp =re.findall(r"(\w+): \"(.+)\"",string)
    if len(temp)>0:
        data[temp[0][0]] = temp[0][1]
        #print(temp)
        continue


print(data)