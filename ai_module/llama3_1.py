import os
import sqlite3
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Template for the Llama model
template = '''
You are mempal, an AI assistant whose purpose is to help the user find jobs. Your primary role is to assist the user and your highest priority is to remember and fulfill his explicit commands unless they violate ethical or legal boundaries.

Here is the context:
{context}

Question: {question}

Answer:
'''
model = OllamaLLM(model="gemma2:27b")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def fetch_user_info(user_id, cursor):
    """Fetch user-specific information from p_info, offers, and applications tables."""
    try:
        # Fetch personal info
        cursor.execute(
            "SELECT first_name, last_name, email, background FROM p_info WHERE user_id = ?",
            (user_id,)
        )
        personal_info = cursor.fetchone()
        if personal_info:
            first_name, last_name, email, background = personal_info
            personal_info_str = f"User's Name: {first_name} {last_name}\nEmail: {email}\nBackground: {background if background else 'N/A'}"
        else:
            personal_info_str = "Personal Info: Not available."

        # Fetch offers
        cursor.execute(
            "SELECT position, company, offer, about, url, status, response FROM offers WHERE user_id = ?",
            (user_id,)
        )
        offers = cursor.fetchall()
        if offers:
            offers_str = "Job Offers:\n" + "\n".join(
                f"- Position: {row[0]} at {row[1]}\n  Offer: {row[2]}\n  About: {row[3]}\n  URL: {row[4]}\n  Status: {'Accepted' if row[5] == 1 else 'Pending'}\n  Response: {'Yes' if row[6] else 'No'}"
                for row in offers
            )
        else:
            offers_str = "Job Offers: No offers available."

        # Fetch applications
        cursor.execute(
            "SELECT resume, offer_id FROM applications WHERE user_id = ?",
            (user_id,)
        )
        applications = cursor.fetchall()
        if applications:
            applications_str = "Applications:\n" + "\n".join(
                f"- Resume: {row[0]}\n  Offer ID: {row[1]}"
                for row in applications
            )
        else:
            applications_str = "Applications: No applications available."

        return f"{personal_info_str}\n\n{offers_str}\n\n{applications_str}"

    except Exception as e:
        print(f"Database Error: {str(e)}")
        return "Additional Information: Could not retrieve user data."

def fetch_chat_log(user_id, cursor):
    """Fetches the full chat log for the given user from the database."""
    try:
        cursor.execute(
            "SELECT user_input, assistant_response FROM chat_log WHERE user_id = ? ORDER BY created_at ASC",
            (user_id,)
        )
        rows = cursor.fetchall()
        chat_log_str = "\n".join(
            f"User: {row[0]}\nMempal: {row[1]}"
            for row in rows
        )
        return chat_log_str if chat_log_str else "No previous conversations found."
    except Exception as e:
        print(f"Database Error: {str(e)}")
        return "No previous conversations found."

def help_mempal(user_id):
    load_dotenv()

    # SQLite connection setup
    conn = sqlite3.connect('ak47.db')  # Connect to your SQLite database
    cursor = conn.cursor()

    help_chat = tk.Tk()
    help_chat.title("Mempal Assistant")

    window_width = 1024
    window_height = 768
    center_window(help_chat, window_width, window_height)

    def on_back():
        help_chat.destroy()
        from menu import open_menu
        open_menu(user_id)

    def open_chat_log():
        """Opens a new window displaying the user's chat log."""
        chat_log_window = tk.Toplevel(help_chat)
        chat_log_window.title("Chat Log")

        chat_log_text = ScrolledText(chat_log_window, wrap=tk.WORD, state=tk.NORMAL, bg="white", fg="black", font=("Arial", 12))
        chat_log_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        chat_log_text.insert(tk.END, fetch_chat_log(user_id, cursor))
        chat_log_text.config(state=tk.DISABLED)

    chat_display = ScrolledText(help_chat, wrap=tk.WORD, state=tk.DISABLED, bg="white", fg="black", font=("Arial", 12))
    chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    user_entry = tk.Entry(help_chat, font=("Arial", 12))
    user_entry.pack(padx=10, pady=10, fill=tk.X)

    def get_mempal_response(user_input):
        context = fetch_chat_log(user_id, cursor) + "\n\n" + fetch_user_info(user_id, cursor)
        result = chain.invoke({'context': context, 'question': user_input})
        return result

    def insert_into_db(user_input, response):
        try:
            cursor.execute(
                "INSERT INTO chat_log (user_input, assistant_response, user_id) VALUES (?, ?, ?)",
                (user_input, response, user_id)
            )
            conn.commit()
        except Exception as e:
            print(f"Database Error: {str(e)}")

    def send_message(event=None):
        user_input = user_entry.get().strip()
        if user_input:
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"YOU: {user_input}\n")
            chat_display.config(state=tk.DISABLED)

            response = get_mempal_response(user_input)
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"Mempal: {response}\n\n")
            chat_display.config(state=tk.DISABLED)

            insert_into_db(user_input, response)
            user_entry.delete(0, tk.END)

    user_entry.bind("<Return>", send_message)
    send_button = tk.Button(help_chat, text="Send", command=send_message, font=("Arial", 12))
    send_button.pack(pady=5)

    back_button = tk.Button(help_chat, text="Back", command=on_back, font=("Arial", 12))
    back_button.pack(pady=5)

    chat_log_button = tk.Button(help_chat, text="View Chat Log", command=open_chat_log, font=("Arial", 12))
    chat_log_button.pack(pady=5)

    help_chat.mainloop()
    conn.close()
