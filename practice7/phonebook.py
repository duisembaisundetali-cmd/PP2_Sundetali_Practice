import csv
from connect import conn, cur

def create_table():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name TEXT,
        phone TEXT
    );
    """)
    conn.commit()

def insert_user(name, phone):
    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()

def insert_from_csv(filename):
    with open(filename, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )
    conn.commit()

def show_all():
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    for r in rows:
        print(r)

def search_by_name(name):
    cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s", (f"%{name}%",))
    print(cur.fetchall())

def search_by_phone(prefix):
    cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (prefix + "%",))
    print(cur.fetchall())

def update_user(name, new_name=None, new_phone=None):
    if new_name:
        cur.execute("UPDATE phonebook SET name=%s WHERE name=%s", (new_name, name))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone=%s WHERE name=%s", (new_phone, name))
    conn.commit()

def delete_user(name=None, phone=None):
    if name:
        cur.execute("DELETE FROM phonebook WHERE name=%s", (name,))
    elif phone:
        cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    conn.commit()

# запуск
create_table()

while True:
    print("\n1.Add 2.Show 3.Search 4.Update 5.Delete 6.Exit 7.Load CSV")
    choice = input(">> ")

    if choice == "1":
        name = input("name: ")
        phone = input("phone: ")
        insert_user(name, phone)

    elif choice == "2":
        show_all()

    elif choice == "3":
        t = input("1-name 2-phone: ")
        if t == "1":
            search_by_name(input("name: "))
        else:
            search_by_phone(input("prefix: "))

    elif choice == "4":
        name = input("who: ")
        new_name = input("new name (enter to skip): ")
        new_phone = input("new phone (enter to skip): ")
        update_user(name, new_name or None, new_phone or None)

    elif choice == "5":
        name = input("delete by name: ")
        delete_user(name=name)

    elif choice == "6":
        break

    elif choice == "7":
        insert_from_csv("contacts.csv")
        print("CSV загружен!")

cur.close()
conn.close()