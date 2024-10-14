import tkinter as tk
from tkinter import messagebox
import sqlite3  # Using sqlite3 for SQLite database

status_options = {0: "None", 1: "Open", 2: "Applied", 3: "Rejected", 4: "Accepted"}

def center_window(window, width, height):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')

def delete_offer(offer_id):
    """Deletes the specified offer from the database."""
    try:
        conn = sqlite3.connect("ak47.db")  # Use your SQLite database file
        cur = conn.cursor()

        # Delete the offer
        cur.execute("DELETE FROM offers WHERE id = ?", (offer_id,))
        conn.commit()
        cur.close()
        conn.close()

        messagebox.showinfo("Success", "Offer deleted successfully.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while deleting the offer: {e}")

def open_offer_details(offer_id, user_id):
    import offer  # Ensure the offer module is correctly imported
    offer.open_offer(offer_id, user_id)  # Pass both offer_id and user_id to open_offer

def open_search_results(results, user_id):
    """Displays the search results in a new window."""
    if not results:
        messagebox.showinfo("No Results", "No offers found for the user.")
        return

    result_window = tk.Tk()
    result_window.title("Search Results")
    window_width = 1024
    window_height = 768
    center_window(result_window, window_width, window_height)

    # Create a frame for the scrollbar and the results
    result_frame = tk.Frame(result_window)
    result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create a canvas for the scrolling
    canvas = tk.Canvas(result_frame)
    scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    # Configure the scrollbar
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack the canvas and scrollbar
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Bind mouse wheel to scroll
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    result_window.bind_all("<MouseWheel>", on_mouse_wheel)

    # Display each result in a new label and buttons
    for idx, result in enumerate(results):
        offer_id, position, company, offer_text, status = result
        status_text = status_options.get(status, "Unknown")

        # Create a frame for each offer result
        offer_frame = tk.Frame(scrollable_frame)
        offer_frame.pack(fill=tk.X, padx=10, pady=5)

        result_text = f"{idx + 1}. Position: {position}, Company: {company}, Status: {status_text}"
        tk.Label(offer_frame, text=result_text, anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Select button
        select_button = tk.Button(offer_frame, text="Select", command=lambda id=offer_id: open_offer_details(id, user_id))
        select_button.pack(side=tk.RIGHT)

        # Delete button
        delete_button = tk.Button(offer_frame, text="Delete", command=lambda id=offer_id: delete_offer(id))
        delete_button.pack(side=tk.RIGHT, padx=5)

    # Add a Close button to close the results window
    tk.Button(result_frame, text="Close", command=result_window.destroy).pack(pady=10)

    result_window.mainloop()
