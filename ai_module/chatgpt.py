import openai
import os
import sqlite3
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from dotenv import load_dotenv

def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')

def help_chatgpt(user_id):
    load_dotenv()

    # SQLite connection setup
    conn = sqlite3.connect('ak47.db')  # Connect to your SQLite database
    cursor = conn.cursor()

    help_chat = tk.Tk()
    help_chat.title("ChatGPT Assistant")

    window_width = 1024
    window_height = 768
    center_window(help_chat, window_width, window_height)

    def on_back():
        help_chat.destroy()
        from menu import open_menu
        open_menu(user_id)

    def open_chat_log():
        from chat_log import open_log
        open_log(user_id)  # Pass the user_id to the chat_log module

    api_key = os.getenv('OPENAI_API_KEY')
    messages = [{"role": "system", "content": "You are here to help the user find a job"}]

    chat_log = ScrolledText(help_chat, wrap=tk.WORD, state=tk.DISABLED, bg="white", fg="black", font=("Arial", 12))
    chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    user_entry = tk.Entry(help_chat, font=("Arial", 12))
    user_entry.pack(padx=10, pady=10, fill=tk.X)

    def get_chatgpt_response(messages):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=1.0,
                max_tokens=1000,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    def insert_into_db(user_input, response, user_id):
        try:
            # Insert user input, assistant response, and user_id into the database
            cursor.execute(
                "INSERT INTO chat_log (user_input, assistant_response, user_id) VALUES (?, ?, ?)",  # Use ? for SQLite
                (user_input, response, user_id)
            )
            conn.commit()
        except Exception as e:
            print(f"Database Error: {str(e)}")

    def store_reminder(reminder, user_id):
        try:
            # Insert the reminder into the reminders table (or update the user's info in p_info)
            cursor.execute(
                "INSERT INTO chat_log (user_input, assistant_response, user_id) VALUES (?, ?, ?)",  # Store the reminder
                (f"MIND: {reminder}", f"I will remember this: {reminder}", user_id)
            )
            conn.commit()
        except Exception as e:
            print(f"Database Error while storing reminder: {str(e)}")

    def send_message(event=None):
        user_input = user_entry.get().strip()
        
        if user_input:
            # Check if the user input starts with the codeword 'MIND'
            if user_input.startswith("MIND"):
                reminder = user_input[len("MIND"):].strip()  # Get the reminder after 'MIND'
                store_reminder(reminder, user_id)  # Store the reminder in the database
                response = f"I will remember this: {reminder}"  # Acknowledge the reminder
                chat_log.config(state=tk.NORMAL)
                chat_log.insert(tk.END, f"YOU: {user_input}\nCHAT GPT: {response}\n\n")
                chat_log.config(state=tk.DISABLED)
                return

            # Fetch the user's personal information from p_info
            cur = conn.cursor()
            cur.execute("SELECT first_name, last_name, email, background FROM p_info WHERE user_id=?", (user_id,))
            user_info = cur.fetchone()
            
            # Build user profile string if user_info exists
            if user_info:
                first_name, last_name, email, background = user_info
                user_profile = f"User: {first_name} {last_name}, Email: {email}, Background: {background}"
            else:
                user_profile = "User information is unavailable."
            
            # Fetch the conversation history for the user from chat_log, but limit it to the last N messages
            cur.execute("SELECT user_input, assistant_response FROM chat_log WHERE user_id=? ORDER BY created_at DESC LIMIT 5", (user_id,))
            chat_history = cur.fetchall()
            
            # Build chat history string, limiting it to the most recent 5 messages
            chat_history_str = "\n".join([f"YOU: {chat[0]}\nCHAT GPT: {chat[1]}" for chat in chat_history])
            
            # Construct the system message with user profile and chat history
            system_message = f"""
                You are a helpful assistant. Always remember the user's details:
                {user_profile}
                Previous conversations:
                {chat_history_str}
            """
            
            # Append system message and user input to the messages list
            messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": user_input})
            
            # Display the user input in the chat log
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, f"YOU: {user_input}\n")
            chat_log.config(state=tk.DISABLED)
            
            # Get the response from ChatGPT
            response = get_chatgpt_response(messages)
            
            # Display the assistant's response
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, f"CHAT GPT: {response}\n\n")
            chat_log.config(state=tk.DISABLED)
            
            # Save the conversation into the database
            insert_into_db(user_input, response, user_id)
            
            # Append assistant response to messages
            messages.append({"role": "assistant", "content": response})
            
            # Clear the user input field
            user_entry.delete(0, tk.END)

    user_entry.bind("<Return>", send_message)
    send_button = tk.Button(help_chat, text="Send", command=send_message, font=("Arial", 12))
    send_button.pack(pady=5)

    back_button = tk.Button(help_chat, text="Back", command=on_back, font=("Arial", 12))
    back_button.pack(pady=5)

    # New "Read Log" button to open the chat_log module
    read_log_button = tk.Button(help_chat, text="Read Log", command=open_chat_log, font=("Arial", 12))
    read_log_button.pack(pady=5)

    help_chat.mainloop()

    # Close the database connection when the app is closed
    conn.close()
