import csv
import json
import os
from datetime import datetime
from connect import get_connection, init_db

class PhoneBook:
    def __init__(self):
        self.conn = get_connection()
        self.cur = self.conn.cursor()
    
    def close(self):
        self.cur.close()
        self.conn.close()
    
    # ========== Basic CRUD Operations ==========
    
    def add_contact(self, name, email=None, birthday=None, group_name=None):
        """Add a new contact"""
        try:
            # Get group_id
            group_id = None
            if group_name:
                self.cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
                result = self.cur.fetchone()
                if result:
                    group_id = result[0]
                else:
                    self.cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group_name,))
                    group_id = self.cur.fetchone()[0]
            
            self.cur.execute("""
                INSERT INTO contacts (name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (name, email, birthday, group_id))
            contact_id = self.cur.fetchone()[0]
            self.conn.commit()
            print(f"Contact '{name}' added successfully!")
            return contact_id
        except Exception as e:
            self.conn.rollback()
            print(f"Error adding contact: {e}")
            return None
    
    def add_phone(self, contact_name, phone, phone_type='mobile'):
        """Add phone to existing contact using stored procedure"""
        try:
            self.cur.execute("CALL add_phone(%s, %s, %s)", (contact_name, phone, phone_type))
            self.conn.commit()
            print(f"Phone {phone} added to {contact_name}")
        except Exception as e:
            self.conn.rollback()
            print(f"Error adding phone: {e}")
    
    def move_to_group(self, contact_name, group_name):
        """Move contact to group using stored procedure"""
        try:
            self.cur.execute("CALL move_to_group(%s, %s)", (contact_name, group_name))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error moving contact: {e}")
    
    def show_all_contacts(self):
        """Display all contacts with their phones"""
        self.cur.execute("""
            SELECT c.id, c.name, c.email, c.birthday, g.name as group_name,
                   STRING_AGG(p.phone || ' (' || p.type || ')', ', ') as phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, g.name
            ORDER BY c.name
        """)
        rows = self.cur.fetchall()
        
        if not rows:
            print("No contacts found.")
            return
        
        print("\n" + "="*80)
        print(f"{'ID':<4} {'Name':<20} {'Email':<25} {'Birthday':<12} {'Group':<10} {'Phones'}")
        print("-"*80)
        for row in rows:
            birthday_str = row[3].strftime('%Y-%m-%d') if row[3] else ''
            phones_str = row[5] if row[5] else ''
            print(f"{row[0]:<4} {row[1]:<20} {str(row[2] or ''):<25} {birthday_str:<12} {str(row[4] or ''):<10} {phones_str}")
        print("="*80)
    
    # ========== Search Operations ==========
    
    def search_contacts(self, query):
        """Search using stored function across all fields"""
        try:
            self.cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            rows = self.cur.fetchall()
            
            if not rows:
                print(f"No contacts found matching '{query}'")
                return
            
            print(f"\n=== Search Results for '{query}' ===")
            for row in rows:
                print(f"\n📱 Name: {row[1]}")
                if row[2]:
                    print(f"   Email: {row[2]}")
                if row[3]:
                    print(f"   Birthday: {row[3].strftime('%Y-%m-%d')}")
                if row[4]:
                    print(f"   Group: {row[4]}")
                if row[5]:
                    print(f"   Phones: {row[5]}")
                print(f"   Added: {row[6].strftime('%Y-%m-%d %H:%M')}")
        except Exception as e:
            print(f"Search error: {e}")
    
    def search_by_email(self, email_pattern):
        """Search by email partial match"""
        self.cur.execute("""
            SELECT c.name, c.email, g.name as group_name,
                   STRING_AGG(p.phone || ' (' || p.type || ')', ', ') as phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE c.email ILIKE %s
            GROUP BY c.id, g.name
        """, (f"%{email_pattern}%",))
        rows = self.cur.fetchall()
        
        if not rows:
            print(f"No contacts found with email containing '{email_pattern}'")
        else:
            print(f"\n=== Contacts with email containing '{email_pattern}' ===")
            for row in rows:
                print(f"  Name: {row[0]}, Email: {row[1]}, Group: {row[2]}, Phones: {row[3]}")
    
    def filter_by_group(self, group_name):
        """Filter contacts by group"""
        self.cur.execute("""
            SELECT c.name, c.email, c.birthday, STRING_AGG(p.phone || ' (' || p.type || ')', ', ') as phones
            FROM contacts c
            LEFT JOIN phones p ON c.id = p.contact_id
            JOIN groups g ON c.group_id = g.id
            WHERE g.name = %s
            GROUP BY c.id
            ORDER BY c.name
        """, (group_name,))
        rows = self.cur.fetchall()
        
        if not rows:
            print(f"No contacts found in group '{group_name}'")
        else:
            print(f"\n=== Contacts in Group: {group_name} ===")
            for row in rows:
                print(f"  Name: {row[0]}")
                if row[1]:
                    print(f"    Email: {row[1]}")
                if row[2]:
                    print(f"    Birthday: {row[2].strftime('%Y-%m-%d')}")
                if row[3]:
                    print(f"    Phones: {row[3]}")
                print()
    
    # ========== Pagination with Navigation ==========
    
    def paginated_view(self, limit=10, sort_by='name', group_filter=None):
        """Interactive paginated view"""
        offset = 0
        while True:
            try:
                self.cur.execute("""
                    SELECT * FROM get_paginated_contacts(%s, %s, %s, %s)
                """, (limit, offset, sort_by, group_filter))
                rows = self.cur.fetchall()
                
                if not rows and offset == 0:
                    print("No contacts found.")
                    break
                
                print(f"\n{'='*80}")
                print(f"Page {offset//limit + 1} | Showing {len(rows)} contacts | Sorted by: {sort_by}")
                if group_filter:
                    print(f"Filtering by group: {group_filter}")
                print(f"{'='*80}")
                
                for row in rows:
                    birthday_str = row[3].strftime('%Y-%m-%d') if row[3] else ''
                    phones_str = row[5] if row[5] else ''
                    print(f"\n📱 {row[1]}")
                    if row[2]:
                        print(f"   Email: {row[2]}")
                    if birthday_str:
                        print(f"   Birthday: {birthday_str}")
                    if row[4]:
                        print(f"   Group: {row[4]}")
                    if phones_str:
                        print(f"   Phones: {phones_str}")
                    print(f"   Added: {row[6].strftime('%Y-%m-%d %H:%M')}")
                
                print(f"\n{'='*80}")
                print("[N]ext  [P]revious  [C]hange sort  [Q]uit")
                choice = input(">> ").lower()
                
                if choice == 'n':
                    offset += limit
                elif choice == 'p' and offset >= limit:
                    offset -= limit
                elif choice == 'c':
                    print("Sort by: [1]Name  [2]Birthday  [3]Date Added")
                    sort_choice = input(">> ")
                    if sort_choice == '1':
                        sort_by = 'name'
                    elif sort_choice == '2':
                        sort_by = 'birthday'
                    elif sort_choice == '3':
                        sort_by = 'created_at'
                    offset = 0
                elif choice == 'q':
                    break
                else:
                    if choice == 'p' and offset < limit:
                        print("Already on first page!")
            except Exception as e:
                print(f"Error: {e}")
                break
    
    # ========== Update Operations ==========
    
    def update_contact(self, name, new_name=None, new_email=None, new_birthday=None, new_group=None):
        """Update contact information"""
        updates = []
        params = []
        
        if new_name:
            updates.append("name = %s")
            params.append(new_name)
        if new_email:
            updates.append("email = %s")
            params.append(new_email)
        if new_birthday:
            updates.append("birthday = %s")
            params.append(new_birthday)
        if new_group:
            self.cur.execute("SELECT id FROM groups WHERE name = %s", (new_group,))
            result = self.cur.fetchone()
            if result:
                updates.append("group_id = %s")
                params.append(result[0])
            else:
                self.cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (new_group,))
                updates.append("group_id = %s")
                params.append(self.cur.fetchone()[0])
        
        if updates:
            params.append(name)
            query = f"UPDATE contacts SET {', '.join(updates)} WHERE name = %s"
            self.cur.execute(query, params)
            self.conn.commit()
            print(f"Contact '{name}' updated successfully!")
    
    def delete_contact(self, name=None, phone=None):
        """Delete contact by name or phone number"""
        if name:
            self.cur.execute("DELETE FROM contacts WHERE name = %s RETURNING name", (name,))
            if self.cur.fetchone():
                print(f"Contact '{name}' deleted successfully!")
            else:
                print(f"Contact '{name}' not found.")
        elif phone:
            self.cur.execute("""
                DELETE FROM contacts WHERE id IN 
                (SELECT contact_id FROM phones WHERE phone = %s) RETURNING name
            """, (phone,))
            result = self.cur.fetchone()
            if result:
                print(f"Contact with phone '{phone}' deleted successfully!")
            else:
                print(f"No contact found with phone '{phone}'.")
        self.conn.commit()
    
    # ========== Import/Export Operations ==========
    
    def export_to_json(self, filename="contacts_export.json"):
        """Export all contacts to JSON file"""
        self.cur.execute("""
            SELECT 
                c.name,
                c.email,
                c.birthday,
                g.name as group_name,
                json_agg(json_build_object('phone', p.phone, 'type', p.type)) as phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, g.name
        """)
        
        rows = self.cur.fetchall()
        contacts = []
        
        for row in rows:
            contact = {
                "name": row[0],
                "email": row[1] or "",
                "birthday": row[2].strftime('%Y-%m-%d') if row[2] else "",
                "group": row[3] or "",
                "phones": row[4] if row[4] else []
            }
            contacts.append(contact)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(contacts, f, indent=2, ensure_ascii=False)
        
        print(f"Exported {len(contacts)} contacts to '{filename}'")
    
    def import_from_json(self, filename):
        """Import contacts from JSON file with duplicate handling"""
        if not os.path.exists(filename):
            print(f"File '{filename}' not found!")
            return
        
        with open(filename, 'r', encoding='utf-8') as f:
            contacts = json.load(f)
        
        for contact in contacts:
            # Check if contact exists
            self.cur.execute("SELECT name FROM contacts WHERE name = %s", (contact['name'],))
            exists = self.cur.fetchone()
            
            if exists:
                print(f"Contact '{contact['name']}' already exists.")
                choice = input("Skip (s) or Overwrite (o)? ").lower()
                if choice == 'o':
                    # Delete existing contact and its phones
                    self.cur.execute("DELETE FROM contacts WHERE name = %s", (contact['name'],))
                    self.conn.commit()
                else:
                    continue
            
            # Insert contact
            birthday = contact.get('birthday')
            if birthday and birthday.strip():
                birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
            else:
                birthday = None
            
            group_name = contact.get('group') or 'Other'
            self.cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            group = self.cur.fetchone()
            if group:
                group_id = group[0]
            else:
                self.cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group_name,))
                group_id = self.cur.fetchone()[0]
            
            self.cur.execute("""
                INSERT INTO contacts (name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (contact['name'], contact.get('email'), birthday, group_id))
            contact_id = self.cur.fetchone()[0]
            
            # Insert phones
            for phone_data in contact.get('phones', []):
                self.cur.execute("""
                    INSERT INTO phones (contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (contact_id, phone_data['phone'], phone_data['type']))
            
            self.conn.commit()
            print(f"Imported contact: {contact['name']}")
    
    def import_from_csv(self, filename):
        """Import contacts from CSV with extended fields"""
        if not os.path.exists(filename):
            print(f"File '{filename}' not found!")
            return
        
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    name = row[0]
                    phone = row[1] if len(row) > 1 else None
                    email = row[2] if len(row) > 2 else None
                    birthday = row[3] if len(row) > 3 and row[3] else None
                    group = row[4] if len(row) > 4 else 'Other'
                    phone_type = row[5] if len(row) > 5 else 'mobile'
                    
                    if birthday:
                        try:
                            birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
                        except:
                            birthday = None
                    
                    # Check if contact exists
                    self.cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
                    exists = self.cur.fetchone()
                    
                    if exists:
                        choice = input(f"Contact '{name}' exists. Skip (s) or Overwrite (o)? ").lower()
                        if choice == 'o':
                            self.cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
                            self.conn.commit()
                        else:
                            continue
                    
                    # Get or create group
                    self.cur.execute("SELECT id FROM groups WHERE name = %s", (group,))
                    group_result = self.cur.fetchone()
                    if group_result:
                        group_id = group_result[0]
                    else:
                        self.cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group,))
                        group_id = self.cur.fetchone()[0]
                    
                    # Insert contact
                    self.cur.execute("""
                        INSERT INTO contacts (name, email, birthday, group_id)
                        VALUES (%s, %s, %s, %s) RETURNING id
                    """, (name, email, birthday, group_id))
                    contact_id = self.cur.fetchone()[0]
                    
                    # Add phone
                    if phone:
                        self.cur.execute("""
                            INSERT INTO phones (contact_id, phone, type)
                            VALUES (%s, %s, %s)
                        """, (contact_id, phone, phone_type))
                    
                    self.conn.commit()
                    print(f"Imported contact: {name}")

# ========== Main Menu ==========

def main():
    # Initialize database
    try:
        init_db()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Note: {e}")
    
    pb = PhoneBook()
    
    while True:
        print("\n" + "="*60)
        print("📞 PHONEBOOK EXTENDED - MAIN MENU")
        print("="*60)
        print("1. Add Contact")
        print("2. Add Phone to Contact")
        print("3. Move Contact to Group")
        print("4. Show All Contacts")
        print("5. Search Contacts")
        print("6. Search by Email")
        print("7. Filter by Group")
        print("8. Update Contact")
        print("9. Delete Contact")
        print("10. Paginated View")
        print("11. Export to JSON")
        print("12. Import from JSON")
        print("13. Import from CSV")
        print("0. Exit")
        print("="*60)
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            name = input("Name: ")
            email = input("Email (optional): ") or None
            birthday = input("Birthday (YYYY-MM-DD, optional): ") or None
            group = input("Group (Family/Work/Friend/Other, default: Other): ") or "Other"
            pb.add_contact(name, email, birthday, group)
            
            # Ask if user wants to add phone
            add_phone = input("Add phone number? (y/n): ").lower()
            if add_phone == 'y':
                phone = input("Phone number: ")
                phone_type = input("Type (home/work/mobile, default mobile): ") or "mobile"
                pb.add_phone(name, phone, phone_type)
        
        elif choice == "2":
            name = input("Contact name: ")
            phone = input("Phone number: ")
            phone_type = input("Type (home/work/mobile): ") or "mobile"
            pb.add_phone(name, phone, phone_type)
        
        elif choice == "3":
            name = input("Contact name: ")
            group = input("Group name: ")
            pb.move_to_group(name, group)
        
        elif choice == "4":
            pb.show_all_contacts()
        
        elif choice == "5":
            query = input("Enter search term: ")
            pb.search_contacts(query)
        
        elif choice == "6":
            email_pattern = input("Enter email pattern (e.g., gmail): ")
            pb.search_by_email(email_pattern)
        
        elif choice == "7":
            print("Available groups: Family, Work, Friend, Other")
            group = input("Enter group name: ")
            pb.filter_by_group(group)
        
        elif choice == "8":
            name = input("Contact name to update: ")
            print("Leave blank to keep current value")
            new_name = input("New name: ") or None
            new_email = input("New email: ") or None
            new_birthday = input("New birthday (YYYY-MM-DD): ") or None
            new_group = input("New group: ") or None
            pb.update_contact(name, new_name, new_email, new_birthday, new_group)
        
        elif choice == "9":
            print("Delete by:")
            print("1. Name")
            print("2. Phone number")
            del_choice = input("Choice: ")
            if del_choice == "1":
                name = input("Contact name: ")
                pb.delete_contact(name=name)
            elif del_choice == "2":
                phone = input("Phone number: ")
                pb.delete_contact(phone=phone)
        
        elif choice == "10":
            limit = int(input("Items per page (default 10): ") or 10)
            print("Sort by: [1]Name  [2]Birthday  [3]Date Added")
            sort_choice = input(">> ")
            sort_by = 'name'
            if sort_choice == '2':
                sort_by = 'birthday'
            elif sort_choice == '3':
                sort_by = 'created_at'
            
            filter_group = input("Filter by group (optional, press Enter to skip): ") or None
            
            pb.paginated_view(limit, sort_by, filter_group)
        
        elif choice == "11":
            filename = input("Export filename (default: contacts_export.json): ") or "contacts_export.json"
            pb.export_to_json(filename)
        
        elif choice == "12":
            filename = input("Import filename (default: contacts_export.json): ") or "contacts_export.json"
            pb.import_from_json(filename)
        
        elif choice == "13":
            filename = input("CSV filename (default: contacts.csv): ") or "contacts.csv"
            pb.import_from_csv(filename)
        
        elif choice == "0":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice!")
    
    pb.close()

if __name__ == "__main__":
    main()