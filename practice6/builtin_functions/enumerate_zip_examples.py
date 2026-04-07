#The enumerate() function takes a collection (e.g. a tuple) and returns it as an enumerate object.
#The enumerate() function adds a counter as the key of the enumerate object.

#Syntax - enumerate(iterable, start)
#Convert a tuple into an enumerate object:
x = ('apple', 'banana', 'cherry')
y = enumerate(x)

seasons = ['Spring', 'Summer', 'Fall', 'Winter']
list(enumerate(seasons))
list(enumerate(seasons, start=1))

def enumerate(iterable, start=0):
    n = start
    for elem in iterable:
        yield n, elem
        n += 1

#The zip() function returns a zip object, which is an iterator of tuples where the first item in each passed iterator is paired together, and then the second item in each passed iterator are paired together etc.
a = ("John", "Charles", "Mike")
b = ("Jenny", "Christy", "Monica")
x = zip(a, b) 

#If one tuple contains more items, these items are ignored:
a = ("John", "Charles", "Mike")
b = ("Jenny", "Christy", "Monica", "Vicky")
x = zip(a, b) 