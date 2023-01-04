import tkinter as tk
import mysql.connector
import tkinter.messagebox as box
from tkinter import ttk
from PIL import Image, ImageTk
import threading

def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

#Splash Screen
splash_root = tk.Tk()
splash_root.geometry('300x250')
window = tk.Tk()
window.title("Library Book Manager")
book_window = tk.Toplevel(window)
book_window.withdraw()
window.withdraw()
splash_root.overrideredirect(True)
splash_root.attributes('-topmost', True)
center(splash_root)


image = Image.open('/Users/sunil390/Documents/GitHub/LibraryManagement/icon.png')
img = image.resize((200,200))
my_img = ImageTk.PhotoImage(img)
tk.Label(splash_root, image = my_img).pack()
lol = tk.Label(splash_root, text='Simplifying Software', font='Terminal 15 italic')
#lol.place(relx=0, rely=20, anchor=tk.CENTER)
lol.pack(side=tk.BOTTOM)
def main():
    global splash_root
    global window
    global book_window
    splash_root.destroy()
    window.deiconify()
    center(window)
    book_window.deiconify()
i=1
def update():
    threading.Timer(0.5, update).start()
    global i 
    global lol
    lol['text'] = lol['text'][:20] + i%3*'.'
    i+=1
splash_root.after(0, update)

splash_root.after(5000, main)

def save_book():
    # Insert the book into the database
    title = title_entry.get()
    author = author_entry.get()
    genre = genre_entry.get()
    if not year_entry.get().isnumeric():
        box.showerror('Error', 'Please enter a valid year')
        return
    year = int(year_entry.get())
    query = "INSERT INTO books (title, author, genre, year) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (title, author, genre, year))
    cnx.commit()
    # Add the book to the list
    #book_list.insert(tk.END, title)
    tree.insert('', tk.END, values=(title, author, genre, year))
    title_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
# Connect to the database
cnx = mysql.connector.connect(user='root', password='<password>', #<password>
                              host='localhost', database='library')

# Create the main window


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
        for (title, author, genre, year) in cursor:
            tree.insert('', tk.END, values=(title, author, genre, year))

def cancel():
    global cursor
    global tree
    for child in tree.get_children():
        tree.delete(child)
    cursor.execute(f'select * from books')
    for (title, author, genre, year) in cursor:
        tree.insert('', tk.END, values=(title, author, genre, year))

tk.Button(book_frame, text="Delete", command=delete).pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Add a listbox to display the book list
#book_list = tk.Listbox(book_frame, yscrollcommand=scrollbar.set)
#book_list.pack(side=tk.LEFT, fill=tk.BOTH)
#scrollbar.config(command=book_list.yview)

#Tree
tree = ttk.Treeview(book_frame, columns=('Title', 'Author', 'Genre', 'Year'), show='headings')
tree.heading('Title', text='Book Name')
tree.heading('Author', text='Author')
tree.heading('Genre', text='Genre')
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
cursor.execute("create table if not exists books(Title varchar(50), Author varchar(20), Genre varchar(25), Year int)")
query = "SELECT * FROM books"
cursor.execute(query)
for (title,author, genre, year) in cursor:
    tree.insert('', tk.END, values=(title ,author, genre, year))

# Add a frame for the buttons
button_frame = tk.Frame(window)
button_frame.pack()

title_entry = None
author_entry = None
year_entry = None

# Add a button to add a book

# Display a dialog to get the book details
book_window.title("Add Book")
tk.Label(book_window, text="Title:").grid(row=0, column=0)
title_entry = tk.Entry(book_window)
title_entry.grid(row=0, column=1)
tk.Label(book_window, text="Author:").grid(row=1, column=0)
author_entry = tk.Entry(book_window)
author_entry.grid(row=1, column=1)
tk.Label(book_window, text="Genre:").grid(row=2, column=0)
genre_entry = tk.Entry(book_window)
genre_entry.grid(row=2, column=1)
tk.Label(book_window, text="Year:").grid(row=3, column=0)
year_entry = tk.Entry(book_window)
year_entry.grid(row=3, column=1)
tk.Button(book_window, height=8, width=2, text="Save", command=save_book).grid(row=0, column=3, rowspan=4)

tk.mainloop()
#prawnsux
