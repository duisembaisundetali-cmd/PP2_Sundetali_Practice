students = [
    {"name": "Ali", "grade": 85},
    {"name": "Dana", "grade": 92},
    {"name": "Max", "grade": 78}
]
sorted_students = sorted(students, key=lambda student: student["grade"])
print(sorted_students)