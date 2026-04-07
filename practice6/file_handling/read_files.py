#The key function for working with files in Python is the open() function.
#The open() function takes two parameters; filename, and mode.
#There are four different methods (modes) for opening a file:
    #"r" - Read - Default value. Opens a file for reading, error if the file does not exist
    #"a" - Append - Opens a file for appending, creates the file if it does not exist
    #"w" - Write - Opens a file for writing, creates the file if it does not exist
    #"x" - Create - Creates the specified file, returns an error if the file exist
    #"t" - Text - Default value. Text mode
    #"b" - Binary - Binary mode (e.g. images)

#The open() function returns a file object, which has a read() method for reading the content of the file:
f = open("demofile.txt")
print(f.read()) 

#Open a file on a different location:
f = open("D:\\myfiles\welcome.txt")
print(f.read()) 

#Using the with keyword:
with open("demofile.txt") as f:
  print(f.read()) 

#Close the file when you are finished with it:
f = open("demofile.txt")
print(f.readline())
f.close() 

#By default the read() method returns the whole text, but you can also specify how many characters you want to return:
#Return the 5 first characters of the file:
with open("demofile.txt") as f:
  print(f.read(5)) 

#Read one line of the file:
with open("demofile.txt") as f:
  print(f.readline()) 

#Read two lines of the file:
with open("demofile.txt") as f:
  print(f.readline())
  print(f.readline()) 

#Loop through the file line by line:
with open("demofile.txt") as f:
  for x in f:
    print(x)