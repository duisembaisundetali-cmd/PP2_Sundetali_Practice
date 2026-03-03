#
import re
txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)
if x:
    print("YEEESS!!!")
else:
    print("NOOOOO!!!")
#
import re

txt = "The rain in Spain"
x = re.findall("ai", txt)
print(x)
#
import re

txt = "The rain in Spain"
x = re.search("\s", txt)

print("The first white-space character is located in position:", x.start())
#
import re

txt = "The rain in Spain"
x = re.split("\s", txt)
print(x)
#
import re

txt = "The rain in Spain"
x = re.sub("\s", "9", txt)
print(x)
#
import re

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.span())
#
import re

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.string)
#
import re

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.group())
