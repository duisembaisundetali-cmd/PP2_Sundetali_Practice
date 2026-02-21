# function
def greet(name):
    print("Hello",name)
greet("Emil")
# lambda
x= lambda a,b,c:a*b*c
print(x(3,4,5))
# *args
def kbtu(*course):
    print("he study at "+course[0]+" course")
kbtu("first","second","third","fourth")
# **kwargs
def myfunc(**name):
    print("his name is "+name["fname"])
myfunc(fname="Sunya",lname="duisembai")
#class
class kbtu:
    name="Sundetali"
    course=1
    major="information system"
x=kbtu()
print("My name is ",x.name )
print("i study at ",x.course)
print("My majority is ",x.major)
#