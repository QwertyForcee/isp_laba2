import types

class MySerializer:
    def func_to_valid(self,f):
        obj = f.__code__
        new_local = list(obj.co_varnames)
        new_varnames = list(obj.co_varnames)
        new_co_names = list(obj.co_names)
        new_co_consts = list(obj.co_consts)
        from __main__ import __dict__ as md
        #for n in obj.co_names:
        #    if n in md and not n in obj.co_varnames:
        #        new_varnames.append(n)
        #        new_co_consts.append(md[n])
        #        new_co_names.remove(n)
                
        newobj = types.CodeType(obj.co_argcount,
            obj.co_posonlyargcount,
            obj.co_kwonlyargcount,
            len(obj.co_varnames),#len(new_varnames),
            obj.co_stacksize,
            obj.co_flags,
            obj.co_code,
            obj.co_consts,#tuple(new_co_consts),
            obj.co_names,#tuple(new_co_names),
            obj.co_varnames,#tuple(new_varnames),
            obj.co_filename,
            obj.co_name,
            obj.co_firstlineno,
            obj.co_lnotab,
            obj.co_freevars,
            obj.co_cellvars)
        result = types.FunctionType(newobj,md,f.__name__)
        result()
        return result
        

        
                

def f1(code_obj):
    from __main__ import __dict__
    globals = __dict__
    print(globals)
    #exec(code_obj)