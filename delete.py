code = b't\x00t\x01\x83\x01\x01\x00d\x00S\x00'
#res = code.encode('latin-1')
print(code)
code = list(code)
print(code)
code = bytes(code)
# = [ 124, 0, 106, 0, 114, 12, 100, 1, 124, 0, 95, 0, 100, 0, 83, 0,]
print(code)
#print(bytes(a))

#print(res)