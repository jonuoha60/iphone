from tkinter import *
from tkinter import ttk
from utils.math import add, subtract, multiply, divide, modulo

BACKGROUND_COLOR = "#F5F5F7"      
CARD_COLOR = "#FFFFFF"            
PRIMARY_COLOR = "#007AFF"           
TEXT_PRIMARY = "#000000"            
TEXT_SECONDARY = "#86868B"          
BUTTON_COLOR = "#007AFF"            
BUTTON_HOVER = "#0051D5"            
SUCCESS_COLOR = "#34C759"           
ERROR_COLOR = "#FF3B30"             

window = Tk()
window.configure(bg=BACKGROUND_COLOR)
window.geometry("600x700")
window.title("Calculator")
window.resizable(False, False)

# Style the notebook
style = ttk.Style()
style.theme_use('clam')
style.configure('TNotebook', background=BACKGROUND_COLOR, borderwidth=0)
style.configure('TNotebook.Tab', padding=[20, 10], background=BACKGROUND_COLOR)
style.map('TNotebook.Tab', background=[('selected', CARD_COLOR)])

# Style entry fields
style.configure('TEntry', fieldbackground=CARD_COLOR, background=CARD_COLOR, padding=10)
style.configure('TCombobox', fieldbackground=CARD_COLOR, background=CARD_COLOR)

notebook = ttk.Notebook(window)
tab1 = Frame(notebook, bg=BACKGROUND_COLOR)
notebook.add(tab1, text="Calculator")
notebook.pack(expand=True, fill="both")

# Title
title_label = Label(tab1, text="Calculator", font=("Arial", 28, "bold"), 
                   fg=TEXT_PRIMARY, bg=BACKGROUND_COLOR)
title_label.pack(pady=20)

# Create a card-style frame
card_frame = Frame(tab1, bg=CARD_COLOR, highlightthickness=1, highlightbackground="#E5E5E7")
card_frame.pack(padx=20, pady=10, fill="both", expand=True)

# Subtitle
subtitle_label = Label(card_frame, text="Simple Calculator", font=("Arial", 14, "bold"), 
                      fg=TEXT_PRIMARY, bg=CARD_COLOR)
subtitle_label.pack(pady=(20, 15))

# First number input
num1_label = Label(card_frame, text="First Number", font=("Arial", 12), 
                  fg=TEXT_SECONDARY, bg=CARD_COLOR)
num1_label.pack(anchor="w", padx=20, pady=(10, 5))

entry_num1 = Entry(card_frame, font=("Arial", 12), bg="#F9F9FB", 
                   relief=FLAT, bd=1, insertwidth=2)
entry_num1.pack(padx=20, pady=5, fill="x")

# Operator selection
operator_label = Label(card_frame, text="Operator", font=("Arial", 12), 
                      fg=TEXT_SECONDARY, bg=CARD_COLOR)
operator_label.pack(anchor="w", padx=20, pady=(15, 5))

operators = ["+", "-", "*", "/", "%"]
cb_operator = ttk.Combobox(card_frame, values=operators, state="readonly", 
                          font=("Arial", 12), width=10)
cb_operator.set("+")
cb_operator.pack(padx=20, pady=5, fill="x")

# Second number input
num2_label = Label(card_frame, text="Second Number", font=("Arial", 12), 
                  fg=TEXT_SECONDARY, bg=CARD_COLOR)
num2_label.pack(anchor="w", padx=20, pady=(15, 5))

entry_num2 = Entry(card_frame, font=("Arial", 12), bg="#F9F9FB", 
                   relief=FLAT, bd=1, insertwidth=2)
entry_num2.pack(padx=20, pady=5, fill="x")

# Result display
result_label = Label(card_frame, text="Result: -", font=("Arial", 16, "bold"), 
                    fg=PRIMARY_COLOR, bg=CARD_COLOR)
result_label.pack(pady=20)

# Error message label
error_label = Label(card_frame, text="", font=("Arial", 10), 
                   fg=ERROR_COLOR, bg=CARD_COLOR, wraplength=300)
error_label.pack(pady=5)

def main():
    operator = cb_operator.get()
    error_label.config(text="")
    
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
    except ValueError:
        error_label.config(text="❌ Error: Please enter valid numbers.")
        result_label.config(text="Result: -", fg=ERROR_COLOR)
        return
    
    result = 0
    try:
        if operator == "+":
            result = add(num1, num2)
        elif operator == "-":
            result = subtract(num1, num2)
        elif operator == "*":
            result = multiply(num1, num2)
        elif operator == "/":
            result = divide(num1, num2)
        elif operator == "%":
            result = modulo(num1, num2)
        
        # Format result
        if isinstance(result, float):
            result = round(result, 4)
        
        result_label.config(text=f"Result: {result}", fg=SUCCESS_COLOR)
        error_label.config(text="")
    except ZeroDivisionError:
        error_label.config(text="❌ Error: Cannot divide by zero.")
        result_label.config(text="Result: -", fg=ERROR_COLOR)
    except Exception as e:
        error_label.config(text=f"❌ Error: {str(e)}")
        result_label.config(text="Result: -", fg=ERROR_COLOR)

# Buttons frame
buttons_frame = Frame(tab1, bg=BACKGROUND_COLOR)
buttons_frame.pack(side=BOTTOM, pady=20)

# Calculate button
calculate_button = Button(buttons_frame, text="Calculate", font=("Arial", 14, "bold"), 
                         bg=BUTTON_COLOR, fg="white", command=main, 
                         padx=30, pady=10, relief=FLAT, cursor="hand2",
                         activebackground=BUTTON_HOVER, activeforeground="white")
calculate_button.pack(side=LEFT, padx=5)

# Clear button
def clear_all():
    entry_num1.delete(0, END)
    entry_num2.delete(0, END)
    result_label.config(text="Result: -", fg=PRIMARY_COLOR)
    error_label.config(text="")
    cb_operator.set("+")

clear_button = Button(buttons_frame, text="Clear", font=("Arial", 14, "bold"), 
                     bg="#A2A2A7", fg="white", command=clear_all, 
                     padx=30, pady=10, relief=FLAT, cursor="hand2",
                     activebackground="#8A8A8E", activeforeground="white")
clear_button.pack(side=LEFT, padx=5)

window.mainloop()