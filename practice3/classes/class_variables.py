#
class Person:
  def __init__(self, name):
    self.name = name

  def greet(self):
    print("Hello, my name is " + self.name)

p1 = Person("Emil")
#
class person:
  def __init__(self,name,age):
    self.name=name
    self.age=age
y=person("Ronaldo",41)
del y.age
print(y.name)