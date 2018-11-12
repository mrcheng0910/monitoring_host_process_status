import base64


s1 = base64.encodestring('hello world'+'|||hitnslab|||')
s2 = base64.decodestring(s1)
print s1, s2