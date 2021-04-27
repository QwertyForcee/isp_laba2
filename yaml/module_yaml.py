import yaml

d1 = [
    {'helk':3000,'foo':'bar'},
    {'heeelo':-1,'bar':'foo'},
    [123,132,312,321,213,231],
    ('hello','from','tuple','mptherfcker')
]

d1=['tuple','da','da']
obj = yaml.dump(d1)
print(obj)
