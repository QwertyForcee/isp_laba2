glob=123
glob2=321

def funci():
    print(glob,glob2)

print(funci.__code__.co_names)

print(funci.__globals__)


s="b't\\x00t\\x01\\x83\\x01\\x01\\x00d\\x00S\\x00'"
print( s[2:len(s)-1].encode()  )