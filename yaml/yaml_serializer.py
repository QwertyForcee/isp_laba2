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
            
        elif obj is None:
            return "null"

        else:
            return ""
    
    def dumps(self,obj):
        return self.tovalid(obj)
            

    def _dump_dict(self,obj):
        curtabs = tabs(self.current_indent)
        self.current_indent+=1
        result="\n"
        for item in obj.items():
            result+=curtabs+f"{item[0]}: {self.tovalid(item[1])}\n"
        self.current_indent-=1
        return result

    def _dump_list(self,obj):
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
        self.current_indent-=1            
        return result





class YamlSerializer(Serializer):
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
        