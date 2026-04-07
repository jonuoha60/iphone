def add(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    if num2 != 0:
        return num1 / num2
    else:
        return "Error: Division by zero is not allowed."

def modulo(num1, num2):
    if num2 != 0:
        return num1 % num2
    else:
        return "Error: Modulo by zero is not allowed."

