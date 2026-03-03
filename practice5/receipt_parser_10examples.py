#1
import re

pattern = r"^ab*$"

text = input()
print(bool(re.match(pattern, text)))
#2
import re

pattern = r"^ab{2,3}$"

text = input()
print(bool(re.match(pattern, text)))
#3
import re

pattern = r"[a-z]+_[a-z]+"

text = input()
print(re.findall(pattern, text))
#4
import re

pattern = r"[A-Z][a-z]+"

text = input()
print(re.findall(pattern, text))
#5
import re

pattern = r"^a.*b$"

text = input()
print(bool(re.match(pattern, text)))
#6
import re

text = input()
result = re.sub(r"[ ,\.]", ":", text)

print(result)
#7
import re

def snake_to_camel(text):
    return re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text)

text = input()
print(snake_to_camel(text))
#8
import re

text = input()
result = re.findall(r"[A-Z][a-z]*", text)

print(result)
#9
import re

text = input()
result = re.sub(r"([A-Z])", r" \1", text).strip()

print(result)
#10
import re

text = input()
result = re.sub(r"([A-Z])", r"_\1", text).lower()

print(result)
