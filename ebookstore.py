import sqlite3
db = sqlite3.connect('book')
cursor = db.cursor()

print("------------------\n")
print("\nWelcome to Ebooktore!\n")
# creating the table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS book(id INTEGER PRIMARY KEY, title TEXT,
    author TEXT, qty INTEGER)
''')
db.commit()

cursor = db.cursor()

id1 = 3001
title1 = 'A Tale of Two Cities'
author1 = 'Charles Dickens'
qty1 = 30

id2 = 3002
title2 = 'Harry Potter and the Philosopher\'s Stone'
author2 = 'J.K. Rowling'
qty2 = 40

id3 = 3003
title3 = 'The Lion, The Witch and the Wardrobe'
author3 = 'C.S. Lewis'
qty3 = 25

id4 = 3004
title4 = 'The Lord of the Rings'
author4 = 'J.R.R. Tolkien'
qty4 = 37

id5 = 3005
title5 = 'Alice in Wonderland'
author5 = 'Lewis Carroll'
qty5 = 12

id6 = 3006
title6 = 'Permanent Record'
author6 = 'Edward Snowden'
qty6 = 11

# Could I use a for loop here?
book_entries = [
                (id1,title1,author1,qty1),
                (id2,title2,author2,qty2),
                (id3,title3,author3,qty3),
                (id4,title4,author4,qty4),
                (id5,title5,author5,qty5),
                (id6,title6,author6,qty6),
                ]       

# insert the above list into the table
cursor.executemany('''INSERT OR REPLACE INTO book(id,title,author,qty) VALUES(?,?,?,?)''',
                   book_entries)
db.commit()

# User Menu with while loop to keep coming back here
while True:
    print("***Ebookstore User Menu***")
    print("\n1. Enter book\n2. Update book\n3. Delete book\n4. Search books\n0. Exit\n")
    menu_choice = input("What would you like to do?: ")
    
    # allowing user to enter a new book into the db
    if menu_choice == '1':
        print("\nNew Book Entry")
        while True:
            try:
                new_id = int(input("Enter book ID: "))
            except ValueError:
                print("ID must be a whole number!")
                continue
            else:
                break
     
        new_title = input("Enter book title: ")
        new_author = input("Enter author: ")

        while True:
            try:
                new_qty = int(input("Enter current qty: "))
            except ValueError:
                print("Quantity must be a whole number!")
            else:
                break
    
        cursor.execute('''INSERT OR REPLACE INTO book(id, title, author, qty)
                VALUES(?,?,?,?)''', (new_id, new_title, new_author, new_qty))
        print("\n***New book has been added!***\n")
        
        db.commit()


    # allowing user to update a book
    elif menu_choice == '2':
        print("Update a book: \n")
        id_choice = int(input("Enter the ID of the book you would like to update: "))
        cursor.execute('''SELECT id, title, author, qty FROM book 
            WHERE id = ?''', (id_choice,))
        showbook = cursor.fetchall()
        print(f"\nCurrent book details: ")
        for line in showbook:# using for and line to display the 
                            #book in a more pleasing way to user
            print(f"id:\t{line[0]} \ntitle:\t{line[1]} \nauthor:\t{line[2]} \nqty:\t{line[3]}\n")

        # Sub menu where the user decides what column they would like to update
        update_choice = input('''Which column would you like to update?
                            \n1. ID\n2. Title\n3. Author\n4. Quantity:\n0. Back to menu\n: ''')
        
        if update_choice == '1':
            try:
                updated_id = int(input("What is the new ID?: "))
                cursor.execute('''UPDATE book SET id = ? WHERE id = ? ''', (updated_id, id_choice,))
                db.commit()
                print("\n***ID updated!***\n")
            except ValueError as error:
                print("ID must be a whole number!")
                print(f"Your error is: \"{error}\"")
                db.rollback()
                #******* Is this correct use of rollback?***********
                
        elif update_choice == '2':
            updated_title = input("What is the new title?: ")
            cursor.execute('''UPDATE book SET title = ? WHERE id = ? ''', (updated_title, id_choice,))
            db.commit()
            print("\n***Tile updated!***\n")

        elif update_choice == '3':
            updated_author = input("Who is the new author?: ")
            cursor.execute('''UPDATE book SET author = ? WHERE id = ? ''', (updated_author, id_choice,))
            db.commit()
            print("\n***Author updated!***\n")

        elif update_choice == '4': 
            updated_qty = input("What is the new quantity?: ")
            cursor.execute('''UPDATE book SET qty = ? WHERE id = ? ''', (updated_qty, id_choice,))
            db.commit()
            print("\n***Quantity updated!***\n")

        elif update_choice == '0':
            continue

        else:
            print("Invalid input\n")
            continue
    
    # allowing user to delete a book
    elif menu_choice == '3':
        delete_choice = input("\nPlease enter the ID of the book you would like to delete: ")
        cursor.execute('''DELETE FROM book WHERE id = ? ''', (delete_choice,))
        db.commit() 
        print('Book with ID %s deleted' %delete_choice)

    # allowing user to search the books, either by ID, keyword, or by viewing all books.
    elif menu_choice == '4':
        print("\nSearch Books")
        search_choice = input('''What would you like to search by?:
                              \n1.ID\n2.Author/Title Keyword\n3.Show all books:\n''')

        if search_choice == '1':
            id_choice = input("Enter book ID: ")
            cursor.execute('''SELECT id, title, author, qty FROM book 
            WHERE id = ?''', (id_choice,))
            showbook = cursor.fetchall()
            print(f"\nBook with ID %s: {showbook}" %id_choice)
        
        # I wanted to use a keyword search here, rather than requring the user
        # to enter the exact title, author etc.
        # https://www.geeksforgeeks.org/sql-query-to-match-any-part-of-string/
        elif search_choice == '2':
            keyword = input("Please enter a word from the title of the book or author's name: ")
            cursor.execute(f'''SELECT * FROM book WHERE title LIKE "%{keyword}%"  ''')
            showbook = cursor.fetchall()
            print("Matching titles:\n")
            for line in showbook:
                print(f"id:\t{line[0]} \ntitle:\t{line[1]} \nauthor:\t{line[2]} \nqty:\t{line[3]}\n")
            db.commit()

            cursor.execute(f'''SELECT * FROM book WHERE author LIKE "%{keyword}%" ''')
            showbook = cursor.fetchall()
            print("Matching authors:\n")
            for line in showbook:
                print(f"id:\t{line[0]} \ntitle:\t{line[1]} \nauthor:\t{line[2]} \nqty:\t{line[3]}\n")
            db.commit()

        elif search_choice == '3':
            # I have ordered by author only to demonstrate the ORDER by function
            cursor.execute(f'''SELECT * FROM book ORDER BY author ASC''')
            showbook = cursor.fetchall()
            print("List of all books:")
            for line in showbook:
                print(f"id:\t{line[0]} \ntitle:\t{line[1]} \nauthor:\t{line[2]} \nqty:\t{line[3]}\n")
            
        else:
            print("invalid entry")
            continue

    elif menu_choice == '0':
        db.close()
        print("Goodbye!")
        exit()

    

    
            




    