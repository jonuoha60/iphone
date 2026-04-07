import os
from tkinter import *
from tkinter import ttk

window = Tk()
window.title("Contact Book")
window.geometry('500x500')
note_book = ttk.Notebook(window) 
tab1 = Frame(note_book)
tab2 = Frame(note_book)
note_book.add(tab1, text='Add Contacts')
note_book.add(tab2, text='Contacts')
note_book.pack(expand=1, fill='both')


dummy_contacts = [
    {"name": "Alice Smith", "phone": "123-456-7890", "email": "alice@gmail.com"},
    {"name": "Bob Johnson", "phone": "987-654-3210", "email": "bob@gmail.com"},
]

label = Label(tab1, text="My Contacts", font=("Arial", 16))
label.pack(pady=10)

label_name = Label(tab1, text="Name:")
label_name.pack(pady=5)
entry1 = Entry(tab1)
entry1.pack(pady=5)
label_phone = Label(tab1, text="Phone:")
label_phone.pack(pady=5)
entry2 = Entry(tab1)
entry2.pack(pady=5)
label_email = Label(tab1, text="Email:")
label_email.pack(pady=5)
entry3 = Entry(tab1)
entry3.pack(pady=5)

def add_contact():
    name = entry1.get()
    phone = entry2.get()
    email = entry3.get()
    if name and phone and email:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/contacts.txt"), "a") as file:
            file.write(f"{name} - {phone} - {email}\n")
        contact_info = f"{name} - {phone} - {email}"
        listbox.insert(END, contact_info)
        entry1.delete(0, END)
        entry2.delete(0, END)
        entry3.delete(0, END)
    else:
        error_label = Label(tab1, text="Please fill in all fields", font=("Arial", 12), fg="red")
        error_label.pack(pady=5)

def search_contacts():
    query = entry_search.get().lower()
    listbox.delete(0, END)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/contacts.txt"), "r") as file:
        for line in file:
            if query in line.lower():
                listbox.insert(END, line.strip())



with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/contacts.txt"), "r") as file:
    content = file.read()
    listbox = Listbox(tab2, width=50, height=20)
    listbox.pack(pady=10)
    for line in content.splitlines():
        listbox.insert(END, line)

Button(tab1, text="Add Contact", command=add_contact).pack(pady=10)

label_search = Label(tab2, text="Search Contacts:", font=("Arial", 12))
label_search.pack(pady=5)
entry_search = Entry(tab2)
entry_search.pack(pady=5)
button_search = Button(tab2, text="Search", command=search_contacts)
button_search.pack(pady=5)

window.mainloop()

