#The map() function executes a specified function for each item in an iterable. The item is sent to the function as a parameter.
#Calculate the length of each word in the tuple:
def myfunc(n):
  return len(n)
x = map(myfunc, ('apple', 'banana', 'cherry')) 

#Make new fruits by sending two iterable objects into the function:
def myfunc(a, b):
  return a + b
x = map(myfunc, ('apple', 'banana', 'cherry'), ('orange', 'lemon', 'pineapple')) 


#The filter() function returns an iterator where the items are filtered through a function to test if the item is accepted or not.
#Filter the array, and return a new array with only the values equal to or above 18:
ages = [5, 12, 17, 18, 24, 32]
def myFunc(x):
  if x < 18:
    return False
  else:
    return True
adults = filter(myFunc, ages)
for x in adults:
  print(x) 