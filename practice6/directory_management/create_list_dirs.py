import struct
dir()   # show the names in the module namespace

dir(struct)   # show the names in the struct module




class Shape:
    def __dir__(self):
        return ['area', 'perimeter', 'location']

s = Shape()
dir(s)


import os
os.mkdir("my_folder")

import os
for i in range(3):
    os.mkdir(f"folder_{i}")

import os
files = os.listdir()
print(files)

import os
for item in os.listdir():
    if os.path.isdir(item):
        print(item)

import os
if not os.path.exists("test"):
    os.mkdir("test")