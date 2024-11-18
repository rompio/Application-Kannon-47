import os
import sqlite3  # Use sqlite3 instead of psycopg2
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Define template and model for Llama
template = '''
Answer the Question below.

Here is the context: {context}

Question: {question}

Answer: 
'''

# Initialize the Llama model and prompt
model = OllamaLLM(model="llama3.1")  # Llama model you're using
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')

def help_llama(user_id):
    load_dotenv()

    # SQLite connection setup
    conn = sqlite3.connect('ak47.db')  # Connect to your SQLite database
    cursor = conn.cursor()

    help_chat = tk.Tk()
    help_chat.title("Llama Assistant")

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

    chat_log = ScrolledText(help_chat, wrap=tk.WORD, state=tk.DISABLED, bg="white", fg="black", font=("Arial", 12))
    chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    user_entry = tk.Entry(help_chat, font=("Arial", 12))
    user_entry.pack(padx=10, pady=10, fill=tk.X)

    def get_llama_response(messages):
        # Construct the context and question from messages
        context = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in messages])
        question = messages[-1]['content']  # Get the last user input

        # Use the Llama chain for generating a response
        result = chain.invoke({'context': context, 'question': question})
        return result

    def insert_into_db(user_input, response):
        try:
            # Insert user input, assistant response, and user_id into the database
            cursor.execute(
                "INSERT INTO chat_log (user_input, assistant_response, user_id) VALUES (?, ?, ?)",  # Use ? for SQLite
                (user_input, response, user_id)
            )
            conn.commit()
        except Exception as e:
            print(f"Database Error: {str(e)}")

    def send_message(event=None):
        user_input = user_entry.get().strip()
        if user_input:
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, f"YOU: {user_input}\n")
            chat_log.config(state=tk.DISABLED)
            messages.append({"role": "user", "content": user_input})

            response = get_llama_response(messages)
            chat_log.config(state=tk.NORMAL)
            chat_log.insert(tk.END, f"Llama: {response}\n\n")
            chat_log.config(state=tk.DISABLED)

            # Save the conversation into the database with the user_id
            insert_into_db(user_input, response)

            messages.append({"role": "assistant", "content": response})
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
