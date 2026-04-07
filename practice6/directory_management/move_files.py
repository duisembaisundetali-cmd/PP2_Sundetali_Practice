import shutil
shutil.move("file.txt", "my_folder/file.txt")

import os
os.rename("old.txt", "new.txt")

import os
import shutil
for file in os.listdir():
    if file.endswith(".txt"):
        shutil.move(file, "texts/" + file)

import os
import shutil
for file in os.listdir():
    if file.endswith(".jpg"):
        shutil.move(file, "images/" + file)
    elif file.endswith(".txt"):
        shutil.move(file, "texts/" + file)