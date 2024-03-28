import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create the main window
window = tk.Tk()
window.title("Note Taking App")
window.geometry("600x450")

# Create a text box
note_entry = tk.Text(window)
note_entry.pack()

# Create a save button and database integration
def save_note():
    note_content = note_entry.get("1.0", tk.END).strip()  # Strip leading/trailing whitespace
    if not note_content:
        messagebox.showerror("Error", "Please enter a note before saving.")
        return

    try:
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)")
        cursor.execute("INSERT INTO notes (content) VALUES (?)", (note_content,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Note saved successfully.")
        note_entry.delete("1.0", tk.END)  # Clear the text entry field after saving
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error occurred while saving note: {e}")

save_button = tk.Button(window, text="Save Note", command=save_note)
save_button.pack()

# Adding a button to view saved notes
def view_notes():
    try:
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes")
        notes = cursor.fetchall()
        conn.close()

        view_window = tk.Toplevel(window)
        view_window.title("View Notes")
        view_text = tk.Text(view_window)
        for note in notes:
            view_text.insert(tk.END, note[1] + "\n")
        view_text.pack()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error occurred while fetching notes: {e}")

view_button = tk.Button(window, text="View Notes", command=view_notes)
view_button.pack()

# Adding a button to delete all saved notes
def delete_notes():
    try:
        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS notes")
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "All notes deleted successfully.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error occurred while deleting notes: {e}")

delete_button = tk.Button(window, text="Delete All Notes", command=delete_notes)
delete_button.pack()

# Run the application
window.mainloop()