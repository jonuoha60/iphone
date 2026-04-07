import os
from tkinter import *
from tkinter import ttk

window = Tk()
window.title("Notes")
window.geometry('500x500')
note_book = ttk.Notebook(window) 
tab1 = Frame(note_book)
tab2 = Frame(note_book)
note_book.add(tab1, text='Add Notes')
note_book.add(tab2, text='Notes')
note_book.pack(expand=1, fill='both')


dummy_contacts = [
    {"name": "Alice Smith", "phone": "123-456-7890", "email": "alice@gmail.com"},
    {"name": "Bob Johnson", "phone": "987-654-3210", "email": "bob@gmail.com"},
]

label = Label(tab1, text="My Notes", font=("Arial", 16))
label.pack(pady=10)

label = Label(tab1, text="Note:")
label.pack(pady=5)
entry1 = Entry(tab1)
entry1.pack(pady=5)


def add_contact():
    note = entry1.get()
    
    if note:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/notes.txt"), "a") as file:
            file.write(f"{note}\n")
        listbox.insert(END, note)
        entry1.delete(0, END)
    else:
        error_label = Label(tab1, text="Please fill in all fields", font=("Arial", 12), fg="red")
        error_label.pack(pady=5)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/notes.txt"), "w") as file:
    for note in dummy_contacts:
        file.write(f"{note['name']}\n")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/notes.txt"), "r") as file:
    content = file.read()
    listbox = Listbox(tab2, width=50, height=20)
    listbox.pack(pady=10)
    for line in content.splitlines():
        listbox.insert(END, line)

Button(tab1, text="Add Note", command=add_contact).pack(pady=10)
window.mainloop()

