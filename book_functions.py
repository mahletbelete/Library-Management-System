from database import get_connection
import os

def add_book():
    conn = get_connection()
    cursor = conn.cursor()

    print("\n" + "="*40)
    print("📚        ADD NEW BOOK        ")
    print("="*40)

    # Title
    while True:
        title = input("📝 Enter Title: ").strip()
        if title:
            break
        print("❌ Title required!")

    # Author
    while True:
        author = input("✍️ Enter Author: ").strip()
        if author:
            break
        print("❌ Author required!")

    # Category
    while True:
        category = input("📂 Enter Category: ").strip()
        if category:
            break
        print("❌ Category required!")

    # PDF path (required)
    while True:
        pdf = input("📄 Enter PDF path: ").strip()
        if not pdf:
            print("❌ PDF path required!")
        elif not os.path.exists(pdf):
            print("❌ File does not exist!")
        elif not pdf.lower().endswith(".pdf"):
            print("❌ Must be a PDF file!")
        else:
            break

    # Quantity
    while True:
        quantity = input("🔢 Enter Quantity: ").strip()
        if not quantity:
            print("❌ Quantity required!")
        elif not quantity.isdigit():
            print("❌ Must be a number!")
        elif int(quantity) <= 0:
            print("❌ Must be greater than 0!")
        else:
            quantity = int(quantity)
            break

    cursor.execute(
        "INSERT INTO books(title, author, category, pdf_path, quantity, available) VALUES (?,?,?,?,?,?)",
        (title, author, category, pdf, quantity, 1)
    )

    conn.commit()
    conn.close()

    print(f"✅ '{title}' added successfully! ({quantity} copies)")


def delete_book():
    conn = get_connection()
    cursor = conn.cursor()

    print("\n🗑️ === DELETE BOOK ===")

    # Validate Book ID
    while True:
        book_id = input("🆔 Enter Book ID: ").strip()
        if book_id.isdigit():
            break
        print("❌ Enter valid numeric ID!")

    # Check if book exists
    cursor.execute("SELECT title, quantity FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()

    if not book:
        print("❌ Book not found.")
        conn.close()
        return

    title, quantity = book

    print(f"\n📘 Book: {title}")
    print(f"🔢 Available copies: {quantity}")

    # User choice
    print("\nChoose delete option:")
    print("1 ➖ Delete ONE copy")
    print("2 ❌ Delete ALL copies")

    while True:
        choice = input("👉 Enter choice (1/2): ").strip()
        if choice in ["1", "2"]:
            break
        print("❌ Invalid choice!")

    # OPTION 1 → Delete one copy
    if choice == "1":
        if quantity > 1:
            cursor.execute(
                "UPDATE books SET quantity=? WHERE id=?",
                (quantity - 1, book_id)
            )
            print("🗑️ One copy removed.")
        else:
            confirm = input("⚠️ Only one copy left. Delete completely? (yes/no): ").strip().lower()
            if confirm == "yes":
                cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
                print("🗑️ Book deleted completely.")
            else:
                print("❌ Cancelled.")

    # OPTION 2 → Delete all
    elif choice == "2":
        confirm = input(f"⚠️ Delete ALL copies of '{title}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
            print("🗑️ All copies deleted.")
        else:
            print("❌ Cancelled.")

    conn.commit()
    conn.close()

def view_books(page_size=5):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id,title,author,category,available,quantity FROM books")
    books = cursor.fetchall()

    if not books:
        print("📭 No books in library.")
        conn.close()
        return

    page = 0
    while True:
        start = page*page_size
        end = start + page_size
        page_books = books[start:end]

        print("\n" + "="*60)
        print("📚           LIBRARY BOOKS           ")
        print("="*60)
        print("+----+----------------------+-------------------+-------------+-------+--------+")
        print("| ID | Title                | Author            | Category    | Avail | Qty    |")
        print("+----+----------------------+-------------------+-------------+-------+--------+")

        for b in page_books:
            status = "✅" if b[4] > 0 else "❌"
            print("| {:<2} | {:<20} | {:<17} | {:<11} | {:<5} | {:<6} |".format(
                b[0], b[1][:20], b[2][:17], b[3][:11], status, b[5]
            ))

        print("+----+----------------------+-------------------+-------------+-------+--------+")

        if end >= len(books):
            print("📍 End of list.")
            break

        next_page = input("➡️ Press Enter (next) or 'q' to quit: ").strip().lower()
        if next_page == "q":
            break

        page += 1

    conn.close()


def check_availability():
    conn = get_connection()
    cursor = conn.cursor()

    print("\n🔍 === CHECK AVAILABILITY ===")

    while True:
        title = input("📝 Enter Book Title: ").strip()
        if title:
            break
        print("❌ Title required!")

    cursor.execute("SELECT quantity FROM books WHERE title=?", (title,))
    book = cursor.fetchone()

    if not book:
        print("❌ Book not found.")
    elif book[0] > 0:
        print(f"✅ Available ({book[0]} copies)")
    else:
        print("❌ Not available.")

    conn.close()


def count_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(quantity) FROM books")
    total = cursor.fetchone()[0] or 0

    print("\n📊 === TOTAL BOOKS ===")
    print(f"📚 Total books in library: {total}")

    conn.close()


def save_books_to_file():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    with open("books.txt","w") as file:
        for b in books:
            file.write(str(b)+"\n")

    conn.close()

    print("\n💾 Books saved to 'books.txt' successfully!")


def show_categories():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT category FROM books")
    cats = cursor.fetchall()

    print("\n📂 === BOOK CATEGORIES ===")

    if not cats:
        print("❌ No categories found.")
    else:
        for c in cats:
            print("📁", c[0])

    conn.close()


def recommend_books():
    conn = get_connection()
    cursor = conn.cursor()

    print("\n⭐ === BOOK RECOMMENDATION ===")

    while True:
        category = input("📂 Enter preferred category: ").strip()
        if category:
            break
        print("❌ Category required!")

    cursor.execute("SELECT title FROM books WHERE category=?", (category,))
    books = cursor.fetchall()

    if books:
        print("\n📚 Recommended Books:")
        for b in books:
            print("👉", b[0])
    else:
        print("❌ No books found in this category.")

    conn.close()