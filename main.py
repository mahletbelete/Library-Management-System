from database import create_tables
from auth import register, login
import book_functions as bf
import borrow_functions as br


# input validation for menu
def get_choice(valid):
    while True:
        c = input("👉 Choose: ").strip()
        if c in valid:
            return c
        print("❌ Invalid choice! Try again.")


def admin_menu():
    while True:
        print("\n" + "="*45)
        print("👨‍💼        ADMIN MENU        ")
        print("="*45)
        print("1 📚 Add Book")
        print("2 🗑️  Delete Book")
        print("3 📖 View Books")
        print("4 📊 Count Books")
        print("5 💾 Save Books To File")
        print("6 📂 Book Categories")
        print("7 🚪 Logout")
        print("="*45)

        c = get_choice(["1","2","3","4","5","6","7"])

        if c == "1":
            bf.add_book()

        elif c == "2":
            bf.delete_book()

        elif c == "3":
            bf.view_books()

        elif c == "4":
            bf.count_books()

        elif c == "5":
            bf.save_books_to_file()   # ✅ added

        elif c == "6":
            bf.show_categories()

        elif c == "7":
            print("👋 Logging out...")
            break


def librarian_menu():
    while True:
        print("\n" + "="*45)
        print("📚      LIBRARIAN MENU      ")
        print("="*45)
        print("1 📖 View Books")
        print("2 🔍 Check Availability")
        print("3 📋 Issued Books")
        print("4 🚪 Logout")
        print("="*45)

        c = get_choice(["1","2","3","4"])

        if c == "1":
            bf.view_books()

        elif c == "2":
            bf.check_availability()

        elif c == "3":
            br.show_issued_books()

        elif c == "4":
            print("👋 Logging out...")
            break


def student_menu(username):
    while True:
        print("\n" + "="*45)
        print(f"🎓   STUDENT MENU ({username})   ")
        print("="*45)
        print("1 📖 View Books")
        print("2 📘 Read Book")          # ✅ added
        print("3 📥 Borrow Book")
        print("4 📤 Return Book")
        print("5 📚 My Books")
        print("6 ⭐ Book Recommendation")
        print("7 🚪 Logout")
        print("="*45)

        c = get_choice(["1","2","3","4","5","6","7"])

        if c == "1":
            bf.view_books()

        elif c == "2":
            br.read_book()   # ✅ added

        elif c == "3":
            br.borrow_book(username)

        elif c == "4":
            br.return_book(username)

        elif c == "5":
            br.student_record(username)

        elif c == "6":
            bf.recommend_books()

        elif c == "7":
            print("👋 Logging out...")
            break


def main():

    create_tables()

    while True:
        print("\n" + "="*50)
        print("📚     LIBRARY MANAGEMENT SYSTEM     ")
        print("="*50)
        print("1 📝 Register")
        print("2 🔐 Login")
        print("3 ❌ Exit")
        print("="*50)

        c = get_choice(["1","2","3"])

        if c == "1":
            register()

        elif c == "2":
            role, user = login()

            if role == "Admin":
                admin_menu()

            elif role == "Librarian":
                librarian_menu()

            elif role == "Student":
                student_menu(user)

            else:
                print("❌ Login failed!")

        elif c == "3":
            print("👋 Thank you for using the system!")
            break


main()