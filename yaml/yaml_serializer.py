import sys
sys.path.append('../')
from serializer import Serializer

#can be changed
def tabs(intend):
    return "  "*intend


class Dumper():
    current_indent = 0

    def tovalid(self,obj):
        if isinstance(obj,str):
            return f"\"{obj}\""

        elif isinstance(obj,bool):
            if obj:
                return "true"
            else:
                return "false"

        elif isinstance(obj,(int,float)):
            return f"{obj}"     

        elif isinstance(obj,dict):
            return self._dump_dict(obj)

        elif isinstance(obj,list):
            #self.current_indent+=1
            return self._dump_list(obj)

        elif isinstance(obj,tuple):
            return self._dump_tuple(obj)
            
        elif isinstance(obj,bytes):
            return f"\"{obj}\""
        elif obj is None:
            return "null"

        else:
            return ""
    
    def dumps(self,obj):
        return self.fix(self.tovalid(obj))
            

    def _dump_dict(self,obj):
        if len(obj)==0:
            return "{}"
        curtabs = tabs(self.current_indent)
        self.current_indent+=1
        result="\n"
        for item in obj.items():
            result+=curtabs+f"{item[0]}: {self.tovalid(item[1])}\n"
        self.current_indent-=1
        return result

    def _dump_list(self,obj):
        if len(obj)==0:
            return "[]"
        curtabs = tabs(self.current_indent)
        self.current_indent+=1
        result="\n"
        for item in obj:
            result+=curtabs+f"- {self.tovalid(item)}\n"
        self.current_indent-=1
        return result

    def _dump_tuple(self,obj):
        curtabs = tabs(self.current_indent)
        self.current_indent+=1        
        result= "!!python/tuple\n"
        for item in obj:
            result+=curtabs+f"- {self.tovalid(item)}\n"
        result = result.rstrip('\n')
        self.current_indent-=1            
        return result

    def fix(self,data):
        if data.startswith('\n'):
            data = data.replace('\n','',1)
        data = str.rstrip(data)
        lines = data.split('\n')
        if '' in lines:
            lines.remove('')
        data = '\n'.join(lines)
        return data
        
import re
class Loader():
    def parse_prepare(self,data):
        data = data.split('\n')
        #print(data)
        if '' in data:
            data.remove('')
        tabs_info = list()
        for item in data:
            tabs_info.append((item, len(re.findall(r"( *).+",item)[0])) )
        return tabs_info
        
    
    def parse(self,indent,data,index):
        res = dict()
        cur = indent
        prev = None
        for d in data[index:]:
            cur = d[1]
            if cur == indent:
                temp = self.validtemp(d[0])
                if isinstance(temp,tuple):
                    if temp[0]=='!!python/tuple':
                        prev = temp[1]
                        res.update({temp[1]:tuple()})
                        index+=1
                        continue
                if isinstance(temp,dict):
                    if list(temp.values())[0] is None:
                        prev = list(temp.keys())[0]
                        res.update(temp)
                        index+=1
                        continue
                elif isinstance(temp,list):
                    if isinstance(res,tuple):
                        res = res + temp
                        continue
                    if not isinstance(res,list):
                        res = list()

                    if isinstance(res,list):
                        res += temp
                    continue

                if isinstance(temp,(tuple,dict)) and not isinstance(res,tuple):
                    res[temp[0]] = temp[1]                                    


            elif cur > indent:
                temp = self.parse(cur,data,index)
                if isinstance(res,dict):
                    res[prev] = temp
                elif isinstance(res,tuple):
                    if isinstance(temp,list):
                        res +=tuple(temp)
                    else:
                        res += temp
                elif isinstance(res,list):
                    res+=temp
                
                temp_index = index
                more_items=False
                for item in data[index:]:
                    if item[1] == indent:
                        more_items = True
                        break
                    temp_index+=1                
                if more_items:
                    temp = self.parse(indent,data,temp_index)
                    if isinstance(res,dict):
                        res.update(temp)
                    elif isinstance(res,tuple):
                        res+=tuple(temp)
                    elif isinstance(res,list):
                        res+=temp
                    return res

                else:
                    return  res

            elif cur < indent:
                break
            index+=1        
        return res

    def validtemp(self,string):

        temp = re.findall(r"(\w+): \[\]",string)
        if len(temp)>0:
            return (temp[0],list())
        temp = re.findall(r"(\w+): {}",string)
        if len(temp)>0:
            return (temp[0],dict())
        temp = re.findall(r"(\w+): !!python/tuple",string)
        if len(temp)>0:
            return ('!!python/tuple',temp[0])        

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
                elif value == 'null':
                    res = None
            return (temp[0][0],res)     
        temp =re.findall(r"(\w+): \"(.+)\"",string)
        if len(temp)>0:
            return temp[0]
        temp =re.findall(r"(\w+): ",string)
        if len(temp)>0:
            return {temp[0]:None}

        temp = re.findall(r"- (\w+)",string)
        if len(temp)>0:
            value = temp[0]
            try:
                res = int(value)
            except:
                res = value
                if value == 'true' or value == 'True':
                    res = True
                elif value == 'false' or value == 'False':
                    res = False
            return [res,]

        temp = re.findall(r"- \"(.+)\"",string)
        if len(temp)>0:
            return [temp[0],]
            


    def tovalid(self,data):
        pass
    def loads(self,data):
        obj = self.parse(0,self.parse_prepare(data),0)
        return obj



class YamlSerializer(Serializer):
    def load(self,f):
        data = f.read()
        f.close()
        obj = self.loads(data)
        return obj

    def loads(self,data):
        obj = Loader().loads(data)
        return self.to_valid_obj(obj)
    def dumps(self,obj):
        data = self.to_valid_dict(obj)
        return Dumper().dumps(data)

    def dump(self,obj,f):
        data = self.dumps(obj)
        try:
            f.write(data)
        except Exception:
            print("Exception catched while dumping the data!")
        finally:
            f.close()            
        