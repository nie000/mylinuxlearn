# a='中国'   unicode
# b=b'中国'
# print(a)
# print(b)


a='中国'.encode(encoding='utf-8')
print(a)
b=b'\xe4\xb8\xad\xe5\x9b\xbd'.decode(encoding='utf-8')
print(b)