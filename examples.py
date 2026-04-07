#1
n = int(input())
numbers = list(map(int, input().split()))
sum_of_squares = sum(map(lambda x: x**2, numbers))
print(sum_of_squares)
#2
n = int(input())
numbers = list(map(int, input().split()))
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(len(even_numbers))
#3
n = int(input())
words = input().split()
result = [f"{i}:{word}" for i, word in enumerate(words)]
print(" ".join(result))
#4
n = int(input())
A = list(map(int, input().split()))
B = list(map(int, input().split()))
dot_product = sum(a * b for a, b in zip(A, B))
print(dot_product)
#5
s = input().strip()
vowels = set('aeiou')
has_vowel = any(char.lower() in vowels for char in s)
print("Yes" if has_vowel else "No")