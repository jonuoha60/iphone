from tkinter import *
from tkinter import ttk
from utils.math import add, subtract, multiply, divide, modulo

window= Tk()
window.geometry("500x500") 
window.title("Calculator")
notebook = ttk.Notebook(window)
tab1 = Frame(notebook)
notebook.add(tab1, text="Calculator")
notebook.pack(expand=True, fill="both")

label = Label(tab1, text="Simple Calculator", font=("Arial", 18))
label.pack(pady=20)
operators = ["+", "-", "*", "/", "%"]

entry_num1 = Entry(tab1)
entry_num1.pack(pady=10)

cb_operator = ttk.Combobox(tab1, values=operators, state="readonly")
cb_operator.set("+")  
cb_operator.pack(pady=10)


entry_num2 = Entry(tab1)
entry_num2.pack(pady=10)

label2 = Label(tab1, text="", font=("Arial", 14))
label2.pack(pady=10)

def main():
    operator = cb_operator.get()
    try:
        num1 = int(entry_num1.get())
        num2 = int(entry_num2.get())
    except ValueError:
        label2.config(text="Error: Please enter valid integers.")
        return
    result = 0
    if operator == "+":
        result = add(num1, num2)
        label2.config(text=result)
    elif operator == "-":
        result = subtract(num1, num2)
        label2.config(text=result)
    elif operator == "*":
        result = multiply(num1, num2)
        label2.config(text=result)
    elif operator == "/":
        result = divide(num1, num2)
        label2.config(text=result)
    elif operator == "%":
        result = modulo(num1, num2)
        label2.config(text=result)



Button(tab1, text="Calculate", command=main).pack(pady=10)

window.mainloop()

if __name__ == "__main__":
    main()