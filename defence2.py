#2
a = 3
b = 2
print(a > b)
#4
temperature = 22

if temperature > 30:
  print("It's hot outside!")
elif temperature > 20:
  print("It's warm outside")
elif temperature > 10:
  print("It's cool outside")
else:
  print("It's cold outside!")
#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break
#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)
#1
i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1
#1
i = 1
while i < 6:
  print(i)
  i += 1
  