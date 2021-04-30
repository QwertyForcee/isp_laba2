import sys
sys.path.append('../')
from json_serializer import JsonSerializer

class ExtraAttrsMeta(type):
    def __new__(self,class_name,bases,attrs):
        if not self.filename is None:
            try:
                extra = JsonSerializer().load(open(self.filename))
                attrs.update(extra)          
            except:
                return type(class_name,bases,attrs)

        return type(class_name,bases,attrs)


ExtraAttrsMeta.filename = "bonus.json"

class FirstCombo(metaclass=ExtraAttrsMeta):
    mushroomsPizza = "30cm MushroomsPizza"

ExtraAttrsMeta.filename = "bk_bonus.json"

class SecondCombo(metaclass=ExtraAttrsMeta):
    pepperoni = "30cm Pepperoni"

    
print('FirstCombo',FirstCombo.mushroomsPizza)
print('FirstCombo',FirstCombo.cocaCola)
print('FirstCombo',FirstCombo.mcNuggets)

print('SecondCombo',SecondCombo.pepperoni)
print('SecondCombo',SecondCombo.pepsi)
print('SecondCombo',SecondCombo.whopper)

"""
a = {
    'cheetos':False,
    'cocaCola':"0.5",
    'mcNuggets':"12"
}

JsonSerializer().dump(a,open('bonus.json','w'))
"""
"""
a1 = {
    "pepsi":"Pepsi 2.0",
    "whopper":"Whopper"
}

JsonSerializer().dump(a1,open('bk_bonus.json','w'))
"""
