from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import sqlite3  # Changed to use SQLite
import bcrypt
import sys
import os

# Add the parent directory of the 'roman' folder to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DB_NAME = "ak47.db"  # Changed to use SQLite database file

def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')

def create_db_and_tables():
    """Creates necessary database tables if they do not exist."""
    try:
        conn = sqlite3.connect(DB_NAME)  # Connect to the SQLite database
        cur = conn.cursor()

        # Create the users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            );
        """)

        # Create the p_info table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS p_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                background TEXT,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)

        # Create the offers table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS offers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                position TEXT NOT NULL,
                company TEXT NOT NULL,
                offer TEXT,
                about TEXT,
                url TEXT,
                status INTEGER,
                response BOOLEAN,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)

        # Create the applications table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume TEXT,
                user_id INTEGER,
                offer_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (offer_id) REFERENCES offers(id)
            );
        """)

        # Create the chat_log table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                assistant_response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error creating database tables: {e}")

def login():
    """Handles login action."""
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Please fill in both fields")
        return

    try:
        conn = sqlite3.connect(DB_NAME)  # Connect to the SQLite database
        cur = conn.cursor()

        cur.execute("SELECT id, password FROM users WHERE username=?", (username,))
        user = cur.fetchone()

        if user:
            user_id, stored_hashed_password = user

            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                messagebox.showinfo("Success", "Login successful")
                root.destroy()  # Hide login window
                from menu import open_menu  # Import here to avoid circular import
                open_menu(user_id)  # Call the menu module after login
            else:
                messagebox.showerror("Error", "Invalid credentials")
        else:
            messagebox.showerror("Error", "User not found")

        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def open_register_window():
    """Opens the registration window."""
    root.destroy()  # Hide the login window
    from register import open_register  # Import here to avoid circular import
    open_register()

def on_enter_key(event):
    login()

def open_login():
    """Opens the login window."""
    global username_entry, password_entry, root

    root = tk.Tk()
    root.title("Login")

    window_width = 1024
    window_height = 768

    center_window(root, window_width, window_height)

    # Create a Canvas to place the background image and titles
    canvas = tk.Canvas(root, width=window_width, height=window_height)
    canvas.pack(fill="both", expand=True)

    # Load the background image using Pillow
    try:
        image = Image.open("_images/ak47.png")  
        background_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor="nw", image=background_image)
    except Exception as e:
        print(f"Error loading image: {e}")

    # Add the title and subtitle below the login box
    canvas.create_text(window_width - 620, window_height - 700, text="AK47", font=("Arial", 40, "bold"), fill="white")
    canvas.create_text(window_width - 570, window_height - 650, text="Application Kannon 47", font=("Arial", 20, "bold"), fill="white")

    # Frame for login elements
    login_frame = tk.Frame(root)
    login_frame.place(x=10, y=10)

    tk.Label(login_frame, text="Username").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(login_frame, text="Password").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(login_frame, show='*')
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    login_button = tk.Button(login_frame, text="Login", command=login)
    login_button.grid(row=2, column=1, padx=10, pady=10)

    register_button = tk.Button(login_frame, text="Register", command=open_register_window)
    register_button.grid(row=3, column=1, padx=10, pady=10)

    quit_button = tk.Button(login_frame, text="Quit", command=quit)
    quit_button.grid(row=4, column=1, padx=10, pady=10)

    root.bind('<Return>', on_enter_key)

    root.mainloop()

if __name__ == "__main__":
    create_db_and_tables()
    open_login()
