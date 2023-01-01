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
    #book_list.insert(tk.END, title)
    tree.insert('', tk.END, values=(title, author, year))


# Connect to the database
cnx = mysql.connector.connect(user='root', password='<password>', #<password>
                              host='localhost', database='library')

# Create the main window
window = tk.Tk()
window.title("Library Book Manager")

# Add a frame for the book list
book_frame = tk.Frame(window)
book_frame.pack()

# Add a label and a scrollbar for the book list
tk.Label(book_frame, text="Book List:").pack(side=tk.TOP)
#scrollbar = tk.Scrollbar(book_frame)
#scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# Delete Button (For Book list)
#def delete():
#    global cursor
#    global book_list
#    item = book_list.curselection()
#    if not item:
#        box.showerror('Error', 'Please select a record')
#        return
#    key = book_list.get(item)
#    cursor.execute(f'DELETE FROM books WHERE title="{key}"')
#    cnx.commit()
#    book_list.delete(item)

# Delete Button (For Tree view)
def delete():
    global cursor;
    global tree;
    if not tree.selection():
        box.showerror('Error', 'Please select a record')
        return
    for selected_item in tree.selection():
        key = tree.item(selected_item)['values'][0]
        cursor.execute(f'delete from books where title = "{key}"')
        cnx.commit()
    for selected_item in tree.selection():
        tree.delete(selected_item)  

def find():
    global keyword
    global cursor
    global tree
    s = keyword.get()
    if s:
        for child in tree.get_children():
            tree.delete(child)
        cursor.execute(f'select * from books where title like "%{s}%"')
        for (title, author, year) in cursor:
            tree.insert('', tk.END, values=(title, author, year))

def cancel():
    global cursor
    global tree
    for child in tree.get_children():
        tree.delete(child)
    cursor.execute(f'select * from books')
    for (title, author, year) in cursor:
        tree.insert('', tk.END, values=(title, author, year))

tk.Button(book_frame, text="Delete", command=delete).pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Add a listbox to display the book list
#book_list = tk.Listbox(book_frame, yscrollcommand=scrollbar.set)
#book_list.pack(side=tk.LEFT, fill=tk.BOTH)
#scrollbar.config(command=book_list.yview)

#Tree
tree = ttk.Treeview(book_frame, columns=('Title', 'Author', 'Year'), show='headings')
tree.heading('Title', text='Book Name')
tree.heading('Author', text='Author')
tree.heading('Year', text='Year')
tree.pack(side=tk.BOTTOM)
scrollbar = ttk.Scrollbar(book_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT)

tk.Label(book_frame, text='Search').pack(side=tk.LEFT)
keyword = tk.Entry(book_frame)
keyword.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
keyword.focus_set()
tk.Button(book_frame, text='Search', command=find).pack(side=tk.RIGHT)
tk.Button(book_frame, text='Cancel Search', command=cancel).pack(side=tk.RIGHT)

# Populate the book list
cursor = cnx.cursor()
query = "SELECT * FROM books"
cursor.execute(query)
for (title,author, year) in cursor:
    tree.insert('', tk.END, values=(title ,author, year))

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
lst = []
for child in tree.get_children():        
       lst.append(tree.item(child)["values"][0])

#Searchbox
def Search(name):
    val=name.widget.get()
    print(val)

    if val=='':
        data=lst
    else:
        data=[]
        for item in lst:
            if val.lower() in item.lower():
                data.append(item)
    Update(data)

def Update(data):
    listbox.delete(0,'end')

    for item in data:
        listbox.insert('end',item)

tk.mainloop()
#prawnsux
