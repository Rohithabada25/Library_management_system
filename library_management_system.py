import json


# Store all library books
books = []


# Queue for students waiting for issued books
waiting_queue=[]

# Stack for transcation history
transaction_history=[]


try:
    with open("library_data.json", "r") as file:
        data = json.load(file)

        books = data.get("books", [])
        waiting_queue = data.get("waiting_queue", [])
        transaction_history = data.get("transaction_history", [])



except FileNotFoundError:
    books = []
    waiting_queue = []
    transaction_history = []



# Save library data permanently in JSON file

def save_data():
    with open("library_data.json", "w") as file:
        json.dump({
            "books": books,
            "waiting_queue": waiting_queue,
            "transaction_history": transaction_history
        }, file, indent=4)


# Main menu of the Library Management System

print("==========================================")
print("       LIBRARY MANAGEMENT SYSTEM")
print("==========================================")

while True:
    print("\n1. Add Book")
    print("2. Display Books")
    print("3. Search Book")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. Delete Book")
    print("7. Sort Books")
    print("8. Waiting List")
    print("9. Transaction History")
    print("10. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
       book_id = input("Enter Book ID: ")
       if not book_id.isdigit():
           print("Invalid Book ID! Please enter numbers only.")
           continue

       duplicate = False

       for book in books:
           if book["id"] == book_id:
               duplicate = True
               break

       if duplicate:
            print("Book ID already exists! Please use a different ID.")

       else:
            title = input("Enter Book Title: ")

            if title.strip() == "":
                print("Book Title cannot be empty!")
                continue

            author = input("Enter Author Name: ")

            if author.strip() == "":
                 print("Author Name cannot be empty!")
                 continue

            category = input("Enter Book Category: ")

            if category.strip() == "":
                 print("Book Category cannot be empty!")
                 continue

            book = {
                "id": book_id,
                "title": title,
                "author": author,
                "category": category,
                "available": True
            }

            books.append(book)
            save_data()

            print("Book added successfully!")



    elif choice == "2":
        if len(books) == 0:
           print("No books available in the library.")

        else:
           print("\n========== ALL BOOKS ==========")

        for book in books:
            print("Book ID:", book["id"])
            print("Title:", book["title"])
            print("Author:", book["author"])
            print("Category:", book["category"])

            if book["available"]:
                print("Status: Available")
            else:
                print("Status: Issued")

            print("-------------------------------")





    elif choice == "3":
        search_id = input("Enter Book ID to search: ")

        found = False

        for book in books:
            if book["id"] == search_id:
                print("\nBook Found!")
                print("Book ID:", book["id"])
                print("Title:", book["title"])
                print("Author:", book["author"])
                print("Category:", book["category"])

                if book["available"]:
                    print("Status: Available")
                else:
                    print("Status: Issued")

                found = True
                break

        if not found:
            print("Book not found!")




    elif choice == "4":
        issue_id = input("Enter Book ID to issue: ")

        if not issue_id.isdigit():
            print("Invalid Book ID! Please enter numbers only.")
            continue

        found = False

        for book in books:
            if book["id"] == issue_id:
                found = True

                if book["available"]:
                    student_name = input("Enter Student Name: ")

                    book["available"] = False
                    book["issued_to"] = student_name

                    transaction_history.append(
                        "ISSUED - Book ID: " + book["id"] +
                        " - " + book["title"] +
                        " - Student: " + student_name
                    )

                    save_data()

                    print("Book issued successfully!")
                    print("Issued to:", student_name)

                else:
                    print("Book is already issued.")

                break

        if not found:
            print("Book not found!")



    elif choice == "5":
        return_id = input("Enter Book ID to return: ")
        if not return_id.isdigit():
            print("Invalid Book ID! Please enter numbers only.")
            continue

        found = False

        for book in books:
            if book["id"] == return_id:
                found = True

                if not book["available"]:
                    book["available"] = True
                    save_data()
                    student = book.get("issued_to", "Unknown")

                    print("Book returned successfully!")
                    print("Returned by:", student)

                    transaction_history.append(
                        "RETURNED - Book ID: " + book["id"] +
                        " - " + book["title"] +
                        " - Student: " + student
                    )
                    save_data()

                    book["issued_to"] = ""

                    # Check waiting list
                    next_student = None

                    for person in waiting_queue:
                        if person["book_id"] == return_id:
                            next_student = person
                            break

                    if next_student is not None:
                        print("\nWaiting list found!")
                        print("Next student:", next_student["student"])
                        print("Book is now available for:", next_student["student"])

                        waiting_queue.remove(next_student)

                else:
                    print("Book is already available.")

                break

        if not found:
            print("Book not found!")



    elif choice == "6":
        delete_id = input("Enter Book ID to delete: ")

        found = False

        for book in books:
            if book["id"] == delete_id:
                books.remove(book)
                save_data()
                found = True
                print("Book deleted successfully!")
                break

        if not found:
            print("Book not found!")


     # Bubble Sort is used to sort books       

    elif choice == "7":
        if len(books) == 0:
            print("No books available to sort.")

        else:
            print("\n1. Sort by Book ID")
            print("2. Sort by Book Title")
            print("3. Sort by Author")

            sort_choice = input("Enter your choice: ")

            n = len(books)

            for i in range(n - 1):
                for j in range(n - i - 1):

                    if sort_choice == "1":
                        if int(books[j]["id"]) > int(books[j + 1]["id"]):
                            books[j], books[j + 1] = books[j + 1], books[j]

                    elif sort_choice == "2":
                        if books[j]["title"].lower() > books[j + 1]["title"].lower():
                            books[j], books[j + 1] = books[j + 1], books[j]

                    elif sort_choice == "3":
                        if books[j]["author"].lower() > books[j + 1]["author"].lower():
                            books[j], books[j + 1] = books[j + 1], books[j]

                    else:
                        print("Invalid sorting choice!")
                        break

            if sort_choice in ["1", "2", "3"]:
                print("Books sorted successfully!")


    # Queue follows FIFO (First In, First Out)

    elif choice == "8":
        print("\n1. Add Student to Waiting List")
        print("2. View Waiting List")

        queue_choice = input("Enter your choice: ")

        if queue_choice == "1":
            student_name = input("Enter Student Name: ")
            book_id = input("Enter Book ID: ")

            found = False

            for book in books:
                if book["id"] == book_id:
                    found = True

                    if book["available"]:
                        print("Book is available. You can issue it directly.")
                    else:
                        waiting_queue.append({
                            "student": student_name,
                            "book_id": book_id
                        })

                        save_data()
                        print("Student added to waiting list!")

                    break

            if not found:
                print("Book not found!")

        elif queue_choice == "2":
            if len(waiting_queue) == 0:
                print("Waiting list is empty.")

            else:
                print("\n========== WAITING LIST ==========")

                for person in waiting_queue:
                    print("Student:", person["student"])
                    print("Book ID:", person["book_id"])
                    print("--------------------------------")

        else:
            print("Invalid choice!")



    # Transaction history follows LIFO (Last In, First Out)
    elif choice == "9":
        if len(transaction_history) == 0:
            print("\nNo transactions yet.")

        else:
            print("\n========== TRANSACTION HISTORY ==========")

            for transaction in reversed(transaction_history):
                print(transaction)

            print("==========================================")

    elif choice == "10":
        print("Thank you for using Library Management System!")
        break

    else:
        print("Invalid choice! Please try again.")
