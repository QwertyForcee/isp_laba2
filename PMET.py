glob=123
glob2=321

def funci():
    print(glob,glob2)

print(funci.__code__.co_names)

print(funci.__globals__)