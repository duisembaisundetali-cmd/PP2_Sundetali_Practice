import math
degree=15
n=degree*math.pi/180
print(n)
#2
import math
height=5
base1=5
base2=6
area=(height*(base1+base2))/2
print(area)
#import math

sides = int(input())
length = float(input())

area = (sides * length**2) / (4 * math.tan(math.pi / sides))
print(area)
