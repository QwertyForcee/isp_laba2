import re
def somefunc(indent,data,index):
    res = dict()
    cur = indent
    prev = None
    for d in data[index:]:
        cur = d[1]
        if cur == indent:
            temp = validtemp(d[0])
            if isinstance(temp,dict):
                if temp.items()[0]==None:
                    prev = list(temp.keys())[0]

            res.update(temp)
        elif cur > indent:
            temp = somefunc(cur,data,index)
            res[prev] = temp

        elif cur < indent:
            break
        index+=1        
    return res


def validtemp(string):
    data = dict()

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
        return (temp[0][0],res)         
    temp =re.findall(r"(\w+): \"(.+)\"",string)
    if len(temp)>0:
        return temp[0]
    temp =re.findall(r"(\w+): ",string)
    if len(temp)>0:
        return {temp[0]:None}


res = open('yamla.yml').read()

data = res.split('\n')
#print(data)
tabs_info = list()

for item in data:
    tabs_info.append((item, len(re.findall(r"( *).+",item)[0])) )

result=dict()
cur = 0
#print(tabs_info)

resss = somefunc(0,tabs_info,0)
print(resss)

#data = (string,spacescount)
