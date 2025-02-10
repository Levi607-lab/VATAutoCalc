import tkinter as tk
import pyperclip as pc
import time as t
import threading 
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


result_variable = ""
current_input = ""
is_running = False


def input_converter(*args):
    divisor = vat_entry.get()
    divisor = divisor.replace("%", "")
    output = divisor.replace(".", ",")
    divisor = divisor.replace(",", ".")

    if divisor == "" or not is_number(divisor):
        vat_output.config(text="Please enter a number! \n Default calculation will use 19% VAT.")
        return 1.19
    else:
        vat = ((float(divisor) + 100) / 100)
        vat_output.config(text=f"Using {output}% VAT for calculation.\n")
        return vat
          

def is_number(value):
    global test
    try:
        float(value)
        return True
    except:
        return False    


def calculate_vat():
    global result_variable
    clipboard_content = pc.paste()
    clipboard_content = clipboard_content.replace(',', '.')
    clipboard_content = clipboard_content.replace('€', '')

    if is_number(clipboard_content):
        clipboard_value = float(clipboard_content)
        result = clipboard_value / input_converter()
        result_variable = "{:.2f}".format(result)
        result_variable = result_variable.replace('.', ',')
        pc.copy(result_variable)
        print("The net amount is:", result_variable)
        return result_variable


def update_check():
    global is_running
    while is_running:
        clipboard_content = pc.paste()
        if clipboard_content != result_variable:
            calculate_vat()
        t.sleep(0.5)


def toggle():
    global is_running
    is_running = not is_running

    if not is_running:
        button_start_stop.config(text="Start Auto Calculation")
    else:
        button_start_stop.config(text="Stop Auto Calculation")
        threading.Thread(target=update_check, daemon=True).start()
          

# GUI Setup
root = tk.Tk()
entry_var = tk.StringVar()
root.geometry("350x130+600+250")
root.resizable(False, False)
root.title("VAT Subtractor")

# Row 0: Label, Entry, and "%" Label
vat_label = tk.Label(root, text="VAT Rate:", anchor="w", width=37)
vat_label.grid(row=0, column=0, padx=5, pady=5)

vat_entry = tk.Entry(root, width=5, textvariable=entry_var)
vat_entry.grid(row=0, column=1, padx=5, pady=5)
entry_var.trace_add("write", input_converter)

percent_label = tk.Label(root, text="%")
percent_label.grid(row=0, column=2, padx=5, pady=5)

# Row 1: Output Label
vat_output = tk.Label(root, text="Please enter a number! \n Default calculation will use 19% VAT.")
vat_output.grid(row=1, column=0, padx=5, pady=5, columnspan=3)

# Row 2: Configuration
root.grid_rowconfigure(2, weight=1)

# Row 3: Start/Stop Button
button_start_stop = tk.Button(root, anchor="s", text="Start Auto Calculation", command=toggle)
button_start_stop.grid(row=2, column=0, padx=0, pady=0, columnspan=3)

# Set window icon
root.iconphoto(False, tk.PhotoImage(file=resource_path("vat.png")))

root.mainloop()
