import tkinter as tk
import mysql.connector
import tkinter.messagebox as box
from tkinter import ttk

def save_book():
    # Insert the book into the database
    title = title_entry.get()
    author = author_entry.get()
    year = year_entry.get()
    query = "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)"
    cursor.execute(query, (title, author, year))
    cnx.commit()
    # Add the book to the list
    book_list.insert(tk.END, title)


# Connect to the database
cnx = mysql.connector.connect(user='root', password='<password>',
                              host='localhost', database='library')

# Create the main window
window = tk.Tk()
window.title("Library Book Manager")

# Add a frame for the book list
book_frame = tk.Frame(window)
book_frame.pack()

# Add a label and a scrollbar for the book list
tk.Label(book_frame, text="Book List:").pack(side=tk.TOP)
scrollbar = tk.Scrollbar(book_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Delete Button
def delete():
    global cursor
    global book_list
    item = book_list.curselection()
    if not item:
        box.showerror('Error', 'Please select a record')
        return
    key = book_list.get(item)
    cursor.execute(f'DELETE FROM books WHERE title="{key}"')
    cnx.commit()
    book_list.delete(item)

tk.Button(book_frame, text="Delete", command=delete).pack(side = tk.RIGHT, fill=tk.Y)

# Add a listbox to display the book list
book_list = tk.Listbox(book_frame, yscrollcommand=scrollbar.set)
book_list.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar.config(command=book_list.yview)

# Tree
#tree = ttk.Treeview(book_frame, '', ('Title', 'Author', 'Year'), height=100, name='Book List')
#tree.pack(side=tk.LEFT)

# Populate the book list
cursor = cnx.cursor()
query = "SELECT title FROM books"
cursor.execute(query)
for (title,) in cursor:
    book_list.insert(tk.END, title)

# Add a frame for the buttons
button_frame = tk.Frame(window)
button_frame.pack()

title_entry = None
author_entry = None
year_entry = None

# Add a button to add a book

# Display a dialog to get the book details
book_window = tk.Toplevel(window)
book_window.title("Add Book")
tk.Label(book_window, text="Title:").grid(row=0, column=0)
title_entry = tk.Entry(book_window)
title_entry.grid(row=0, column=1)
tk.Label(book_window, text="Author:").grid(row=1, column=0)
author_entry = tk.Entry(book_window)
author_entry.grid(row=1, column=1)
tk.Label(book_window, text="Year:").grid(row=2, column=0)
year_entry = tk.Entry(book_window)
year_entry.grid(row=2, column=1)
tk.Button(book_window, text="Save", command=save_book).grid(row=5, column=3)

tk.mainloop()