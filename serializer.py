import types
import inspect

class Serializer:
    def to_valid_dict(self,obj):
        if isinstance(obj,types.FunctionType):
            data = self.func_to_valid(obj)
            return data
            
        elif inspect.isclass(obj):
            data = self.class_to_valid(obj)
            return data

        elif str(obj).startswith('<__main__.'): 
            return  self.instance_to_valid(obj)

        elif isinstance(obj,(list,dict,tuple,int,float,str,bool,set)):
            return obj
        else:
            return self.instance_to_valid(obj)


    def to_valid_obj(self,data):
        if str(type(data))=="<class 'dict'>" and 'type' in data.keys():
            if data['type'] == 'function':
                return self.to_valid_func(data['body'])
            if data['type'] == 'class':
                return self.to_valid_class(data['body'])
            else:
                return self.to_valid_instance(data)
        else:
            return data
                

    def func_to_valid(self,obj):
        data = {'type':'function'}
        data['body'] = dict()
        data['body']['modulename'] = obj.__globals__['__name__']
        data['body']['functionname'] = obj.__name__
        data['body']['CodeType']=self._codetype_fill(obj.__code__)
        return data


    def _codetype_fill(self,co):
        #Not for the faint of heart. FUCK MY LIFE
        code_dict = dict()
        code_dict['co_argcount'] = co.co_argcount
        code_dict['co_posonlyargcount'] = co.co_posonlyargcount 
        code_dict['co_kwonlyargcount'] = co.co_kwonlyargcount 
        code_dict['co_nlocals'] = co.co_nlocals 
        code_dict['co_stacksize'] = co.co_stacksize 
        code_dict['co_flags'] = co.co_flags 
        code_dict['co_code'] = co.co_code
        code_dict['co_consts'] = co.co_consts
        code_dict['co_names'] = co.co_names
        code_dict['co_varnames'] = co.co_varnames
        code_dict['co_filename'] = co.co_filename
        code_dict['co_name'] = co.co_name
        code_dict['co_firstlineno'] = co.co_firstlineno
        code_dict['co_lnotab'] = co.co_lnotab
        code_dict['co_freevars'] = co.co_freevars
        code_dict['co_cellvars'] = co.co_cellvars
        
        return code_dict

    def instance_to_valid(self,obj):
        data = {'fields':dict(),'class':self.to_valid_obj(obj.__class__)}
        custom=[o for o in obj.__class__.__dict__.items() if not o[0].startswith('__')]
        for c in custom:
            data[c[0]] = self.to_valid_dict(c[1])
        
        data = {"type":str(obj.__class__),"body":data}
        return data

    def to_valid_instance(self,data):
        obj_class = self.to_valid_obj(data['body']['class'])
        instance = obj_class()
        src = list(data['body']['fields'].values())
        name = data['type']
        for f in list(data["body"]["fields"].items()):
            eval(f"instance.{str(f[0])} = {self.to_valid_obj(f[1])}")

        return instance      

    def class_to_valid(self,obj):
        attributedict = dict()
        custom=[o for o in obj.__dict__.items() if not o[0].startswith('__')]
        for c in custom:
            #attributedict[c[0]] = self.to_valid_dict(c[1])
            attributedict[c[0]] = self.to_valid_dict(c[1])
        data = dict()
        data['type']='class'
        data['body']=dict()
        data['body']['classname'] = obj.__name__       
        data['body']['metaclasses'] = str(obj.__bases__)
        data['body']['attributedict'] = attributedict
        return data

    def to_valid_class(self,data):
        attributedict = dict()
        for a in data['attributedict'].items():
            attributedict[a[0]] = self.to_valid_obj(a[1])
        
        meta = tuple(data['metaclasses'])
        for m in data['metaclasses']:
            if isinstance(m,str):
                meta = (object,)
                

        return type(data['classname'],meta,attributedict)


    def to_valid_func(self,data):

        exec(f"from {data['modulename']} import __dict__ as md")

        co = types.CodeType(
            data['CodeType']['co_argcount'],
            data['CodeType']['co_posonlyargcount'],
            data['CodeType']['co_kwonlyargcount'],
            data['CodeType']['co_nlocals'],
            data['CodeType']['co_stacksize'],
            data['CodeType']['co_flags'],
            bytes(str(data['CodeType']['co_code']),encoding='utf8'),
            tuple(data['CodeType']['co_consts']),
            tuple(data['CodeType']['co_names']),
            tuple(data['CodeType']['co_varnames']),
            data['CodeType']['co_filename'],
            data['CodeType']['co_name'],
            data['CodeType']['co_firstlineno'],
            bytes(str(data['CodeType']['co_lnotab']),'utf8'),
            tuple(data['CodeType']['co_freevars']),
            tuple(data['CodeType']['co_cellvars'])
        )
        result = types.FunctionType(co,eval('md'),data['functionname'])
        return result


                
    