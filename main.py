import tkinter as tk
from tkinter import messagebox
import sqlite3


window = tk.Tk()
window.title("Note Taking App")
window.geometry("600x500")
window.configure(bg="#f0f0f0")  


note_entry = tk.Text(window)
note_entry.pack()


def save_note():
    note_content = note_entry.get("1.0", tk.END).strip()  
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
        note_entry.delete("1.0", tk.END)  
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error occurred while saving note: {e}")

save_button = tk.Button(window, text="Save Note", command=save_note, bg="#4caf50", fg="white")  
save_button.pack()


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

view_button = tk.Button(window, text="View Notes", command=view_notes, bg="#2196f3", fg="white")  
view_button.pack()


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

delete_button = tk.Button(window, text="Delete All Notes", command=delete_notes, bg="#f44336", fg="white")  
delete_button.pack()

# Run the application
window.mainloop()