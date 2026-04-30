from database import get_connection
from getpass import getpass


# username validation (min 2 chars, letters required, numbers optional)
def get_valid_username():
    while True:
        username = input("👤 Username: ").strip()

        if len(username) < 2:
            print("❌ Must be at least 2 characters!")
        elif not any(c.isalpha() for c in username):
            print("❌ Must contain at least one letter!")
        else:
            return username


#  password validation
def get_valid_password():
    while True:
        password = input("🔑 Password: ").strip()

        if len(password) < 2:
            print("❌ Password must be at least 2 characters!")
        else:
            return password


#  role validation
def get_valid_role():
    print("\n🎯 Select Role")
    print("1 👨‍💼 Admin")
    print("2 📚 Librarian")
    print("3 🎓 Student")

    while True:
        choice = input("👉 Choice (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return "Admin" if choice == "1" else "Librarian" if choice == "2" else "Student"
        print("❌ Invalid choice!")


def register():

    conn = get_connection()
    cursor = conn.cursor()

    print("\n" + "="*40)
    print("👤        REGISTER USER        ")
    print("="*40)

    username = get_valid_username()
    password = get_valid_password()
    role = get_valid_role()

    #  LIMIT ADMIN TO 5
    if role == "Admin":
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='Admin'")
        admin_count = cursor.fetchone()[0]

        if admin_count >= 5:
            print("❌ Maximum 5 Admins allowed!")
            conn.close()
            return

    try:
        cursor.execute(
            "INSERT INTO users(username,password,role) VALUES (?,?,?)",
            (username,password,role)
        )
        conn.commit()
        print(f"✅ Registered successfully as {role} 🎉")

    except:
        print("❌ Username already exists!")

    conn.close()

def login():

    conn = get_connection()
    cursor = conn.cursor()

    print("\n" + "="*50)
    print("🔐            LOGIN            ")
    print("="*50)

    username = get_valid_username()
    password = getpass("🔑 Password,\'The values aren't visble for security\':").strip()

    if not password:
        print("❌ Password required!")
        conn.close()
        return None, None

    cursor.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username,password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"✅ Login successful! Welcome {username} 🎉")
        return user[0], username
    else:
        print("❌ Invalid username or password!")
        return None, None