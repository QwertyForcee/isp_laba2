import types
import inspect

class Serializer:
    def to_valid_dict(self,obj):
        if isinstance(obj,types.FunctionType) or isinstance(obj,types.MethodWrapperType):
            data = self.func_to_valid(obj)
            return data
            
        elif inspect.isclass(obj):
            data = self.class_to_valid(obj)
            return data

        elif isinstance(obj,list):
            return [self.to_valid_dict(x) for x in obj]
        elif isinstance(obj,(dict,tuple,int,float,str,bool,set)):
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
            if isinstance(data,list):
                res = list()
                for d in data:
                    res.append(self.to_valid_obj(d))
                return res
            return data
                


    def func_to_valid(self,obj):
        data = {'type':'function'}
        data['body'] = dict()
        data['body']['globals']=dict()
        globs = obj.__globals__.items()
        for g in globs:
            if g[0] in obj.__code__.co_names:
                data['body']['globals'][g[0]]=self.to_valid_dict(g[1])

        data['body']['modulename'] = obj.__globals__['__name__']
        data['body']['functionname'] = obj.__name__
        data['body']['CodeType']=self._codetype_fill(obj.__code__)
        return data


    def _codetype_fill(self,co):
        #Not for the faint of heart.
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
        data = {'fields':dict(),'class':self.to_valid_dict(obj.__class__)}
        custom=[o for o in obj.__class__.__dict__.items() if not o[0].startswith('__')]
        for c in custom:
            data['fields'][c[0]] = self.to_valid_dict(c[1])

        custom=[o for o in obj.__dict__.items() if not o[0].startswith('__')]
        for c in custom:
            data['fields'][c[0]] = self.to_valid_dict(c[1])
        
        data = {"type":str(obj.__class__),"body":data}
        return data

    def to_valid_instance(self,data):
        obj_class = self.to_valid_obj(eval(str(data['body']['class'])))
        extra_attrs= dict()
        for key,value in data['body']['fields'].items():
            setattr(obj_class,key,self.to_valid_obj(value))
        #obj_class.__dict__.update(extra_attrs)
        instance = obj_class()
        #instance.__dict__.update(extra_attrs)
        #src = list(data['body']['fields'].values())
        #name = data['type']
        """
        for f in list(data["body"]["fields"].items()):
            temp = self.to_valid_obj(f[1])
            if inspect.isclass(temp):
                eval(f"instance.{str(f[0])} = temp")
            else:
                eval(f"instance.{str(f[0])} = {temp}")
        """

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
            #if isinstance(attributedict[a[0]],types.MethodWrapperType)
            #    attributedictp[a[0]] = 

        meta = tuple(data['metaclasses'])
        for m in data['metaclasses']:
            if isinstance(m,str):
                meta = (object,)

        return type(data['classname'],meta,attributedict)


    def to_valid_func(self,data):

        #exec(f"from {data['modulename']} import __dict__ as md")

        if isinstance(data['CodeType']['co_code'],list):
            cocode = bytes(data['CodeType']['co_code'])
        else:        
            cocode = (data['CodeType']['co_code'])[2:len(data['CodeType']['co_code'])-1].encode().decode('unicode_escape')
            cocode = cocode.encode('latin-1')


        #cocode = eval(f"""str("{cocode}")""")
        if isinstance(data['CodeType']['co_lnotab'],list):
            colnotab = bytes(data['CodeType']['co_lnotab'])
        else:
            colnotab = (data['CodeType']['co_lnotab'])[2:len(data['CodeType']['co_lnotab'])-1].encode().decode('unicode_escape')
            colnotab = colnotab.encode('latin-1')
        #colnotab = eval(f"""str("{colnotab}")""")

        co = types.CodeType(
            data['CodeType']['co_argcount'],
            data['CodeType']['co_posonlyargcount'],
            data['CodeType']['co_kwonlyargcount'],
            data['CodeType']['co_nlocals'],
            data['CodeType']['co_stacksize'],
            data['CodeType']['co_flags'],
            cocode,
            # bytes(bytearray([(data['CodeType']['co_code'])[2:len(data['CodeType']['co_code'])-1]])),
            tuple(data['CodeType']['co_consts']),
            tuple(data['CodeType']['co_names']),
            tuple(data['CodeType']['co_varnames']),
            data['CodeType']['co_filename'],
            data['CodeType']['co_name'],
            data['CodeType']['co_firstlineno'],
            colnotab,
            # bytes(str(data['CodeType']['co_lnotab']),'utf8'),
            tuple(data['CodeType']['co_freevars']),
            tuple(data['CodeType']['co_cellvars'])
        )
        globs = self.to_valid_obj(data['globals'])
        globs.update({'__module__':data["modulename"]})
        import builtins
        globs.update(builtins.__dict__)
        result = types.FunctionType(co,globs,data['functionname'])
        result.__module__=data["modulename"]
        return result


                
    
