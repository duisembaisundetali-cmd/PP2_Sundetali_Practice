import math
degree=15
n=degree*math.pi/180
print(n)
#2
import datetime
today=datetime.date.today()
five_days_ago=datetime.date.fromordinal(today.toordinal()-5)
print(today)
print(five_days_ago)
#3
def squares(a,b):
    for x in range(a,b+1):
        yield x*x
a=int(input())
b=int(input())
for val in squares(a,b):
    print(val)
#4
import json
x='{"name":"sunya","age":18,"city":"Almaty"}'
y=json.dumps(x)
print(y)