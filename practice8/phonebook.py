from connect import get_connection

def search(pattern):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_pattern(%s)", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def insert_or_update(name, phone):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()


def delete_user(value):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_user(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()


def paginate(limit, offset):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


if __name__ == "__main__":
    print("1 - Search")
    print("2 - Insert/Update")
    print("3 - Delete")
    print("4 - Pagination")

    choice = input("Choose: ")

    if choice == "1":
        pattern = input("Enter search: ")
        search(pattern)

    elif choice == "2":
        name = input("Name: ")
        phone = input("Phone: ")
        insert_or_update(name, phone)

    elif choice == "3":
        value = input("Enter name or phone: ")
        delete_user(value)

    elif choice == "4":
        limit = int(input("Limit: "))
        offset = int(input("Offset: "))
        paginate(limit, offset)