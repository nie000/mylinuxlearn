#变量的机制
a = 300
b = 300
#
c = a
a = 1
print(c)

print(id(c))

print(id(a))

#id(a) id(a)
