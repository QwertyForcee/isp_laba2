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
    MushroomsPizza = "Large"


print(FirstCombo.MushroomsPizza)
print(FirstCombo.CocaCola)
print(FirstCombo.McNuggets)

"""
a = {
    'Cheetos':False,
    'Coca-Cola':"0.5",
    'McNuggets':"12"
}

JsonSerializer().dump(a,open('bonus.json','w'))
"""
temp=123

