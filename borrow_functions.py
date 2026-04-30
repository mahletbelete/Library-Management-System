from database import get_connection
import datetime
import os
import subprocess

def borrow_book(student):
    conn = get_connection()
    cursor = conn.cursor()

    print("\n📥 === BORROW BOOK ===")

    while True:
        book_id = input("🆔 Enter Book ID: ").strip()
        if book_id.isdigit():
            break
        print("❌ Invalid ID!")

    cursor.execute("SELECT quantity, pdf_path, title FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()

    if not book:
        print("❌ Book not found.")
        conn.close()
        return

    if book[0] <= 0:
        print("❌ No copies available.")
        conn.close()
        return

    # DUE DATE
    today = datetime.date.today()
    due_date = today + datetime.timedelta(days=7)

    # reduce quantity
    new_quantity = book[0] - 1
    cursor.execute(
        "UPDATE books SET quantity=?, available=? WHERE id=?",
        (new_quantity, 1 if new_quantity > 0 else 0, book_id)
    )

    cursor.execute(
        "INSERT INTO borrow(student,book_id,issue_date,due_date) VALUES (?,?,?,?)",
        (student, book_id, str(today), str(due_date))
    )

    conn.commit()

    print(f"✅ Borrowed: 📘 '{book[2]}'")
    print(f"⏳ Due Date: {due_date}")
    print(f"⚠️  Late return leads to penality of 5 birr * each day!")


    print("\n📖 Open book? (yes/no)")
    if input("👉 ").strip().lower() == "yes":
        pdf_path = os.path.abspath(book[1])
        if os.path.exists(pdf_path):
            subprocess.Popen(f'"{pdf_path}"', shell=True)
        else:
            print("❌ PDF not found.")

    conn.close()

def return_book(student):
    conn = get_connection()
    cursor = conn.cursor()

    print("\n📤 === RETURN BOOK ===")

    while True:
        book_id = input("🆔 Enter Book ID: ").strip()
        if book_id.isdigit():
            break
        print("❌ Invalid ID!")

    cursor.execute(
        "SELECT issue_date, due_date FROM borrow WHERE student=? AND book_id=?",
        (student, book_id)
    )
    record = cursor.fetchone()

    if not record:
        print("❌ You didn't borrow this book.")
        conn.close()
        return

    # PENALTY LOGIC
    today = datetime.date.today()
    due_date = datetime.datetime.strptime(record[1], "%Y-%m-%d").date()

    if today > due_date:
        late_days = (today - due_date).days
        penalty = late_days * 5
        print(f"⚠️ Late by {late_days} days")
        print(f"💰 Penalty: {penalty} birr")
    else:
        print("✅ Returned on time. No penalty.")

    # delete record
    cursor.execute("DELETE FROM borrow WHERE student=? AND book_id=?", (student, book_id))

    # update quantity
    cursor.execute("SELECT quantity FROM books WHERE id=?", (book_id,))
    qty = cursor.fetchone()[0]

    cursor.execute(
        "UPDATE books SET quantity=?, available=1 WHERE id=?",
        (qty+1, book_id)
    )

    conn.commit()
    conn.close()

    print("📚 Book returned successfully!")

def student_record(student):
    conn = get_connection()
    cursor = conn.cursor()

    print("\n" + "="*40)
    print("📚      MY BORROWED BOOKS      ")
    print("="*40)

    cursor.execute("""
    SELECT books.title, borrow.issue_date, borrow.due_date
    FROM borrow
    JOIN books ON books.id=borrow.book_id
    WHERE student=?
""", (student,))

    records = cursor.fetchall()

    if not records:
        print("📭 You have not borrowed any books.")
    else:
        for r in records:
          print(f"📘 {r[0]} | 📅 {r[1]} | ⏳ Due: {r[2]}")

    conn.close()


def show_issued_books():
    conn = get_connection()
    cursor = conn.cursor()

    print("\n" + "="*50)
    print("📋      ISSUED BOOKS LIST      ")
    print("="*50)

    cursor.execute("SELECT student, book_id, issue_date, due_date FROM borrow")
    data = cursor.fetchall()

    if not data:
        print("📭 No books issued.")
    else:
           for d in data:
               print(f"👤 {d[0]} | 🆔 {d[1]} | 📅 {d[2]} | ⏳ Due: {d[3]}")

    conn.close()


def read_book():
    conn = get_connection()
    cursor = conn.cursor()

    print("\n" + "="*40)
    print("📖         READ BOOK         ")
    print("="*40)

    while True:
        book_id = input("🆔 Enter Book ID: ").strip()
        if not book_id:
            print("❌ Book ID required!")
        elif not book_id.isdigit():
            print("❌ Must be a number!")
        else:
            break

    cursor.execute("SELECT title, pdf_path FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()

    if not book:
        print("❌ Book not found.")
        conn.close()
        return

    pdf_path = os.path.abspath(book[1])

    if not os.path.exists(pdf_path):
        print("❌ PDF file not found.")
        conn.close()
        return

    print(f"📖 Opening: '{book[0]}'...")

    try:
        subprocess.Popen(f'"{pdf_path}"', shell=True)
    except:
        print("❌ Failed to open PDF.")

    conn.close()