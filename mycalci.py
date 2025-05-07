import tkinter as tk
import math
import re
from tkinter import simpledialog

history_list = []
memory = 0

# Colors and fonts
BG_COLOR = "#1e1e2f"
ENTRY_BG = "#2e2e3f"
ENTRY_FG = "#f0f0f5"
BTN_BG_NUM = "#3a3a5a"
BTN_BG_OP = "#56568c"
BTN_BG_FUNC = "#7c7ca1"
BTN_FG = "#f0f0f5"
BTN_HOVER = "#9a9acb"
FONT = ("Segoe UI", 16)
ENTRY_FONT = ("Segoe UI", 24, "bold")

MAX_INPUT_LENGTH = 20
LIMIT_MSG = "Maximum limit reached"

def on_enter(e):
    e.widget['background'] = BTN_HOVER

def on_leave(e):
    btn = e.widget
    text = btn.cget("text")
    if text.isdigit() or text == ".":
        btn['background'] = BTN_BG_NUM
    elif text in ["+", "-", "*", "/", "=", "⌫"]:
        btn['background'] = BTN_BG_OP
    else:
        btn['background'] = BTN_BG_FUNC

def update_history(expression, result):
    history_list.append(f"{expression} = {result}")

def show_history():
    popup = tk.Toplevel(root)
    popup.title("History")
    history_text = tk.Text(popup, width=40, height=15)
    history_text.pack(padx=10, pady=10)
    if history_list:
        for item in history_list[-50:]:
            history_text.insert(tk.END, item + "\n")
    else:
        history_text.insert(tk.END, "No history yet.")
    history_text.config(state=tk.DISABLED)
    tk.Button(popup, text="Close", command=popup.destroy).pack(pady=5)

def preprocess_expression(expr):
    # n n√ x or x n√ n => (x**(1/n))
    expr = re.sub(
        r'(\d+(\.\d+)?)\s*n√\s*(\d+(\.\d+)?)',
        lambda m: f"({m.group(3)}**(1/{m.group(1)}))",
        expr
    )
    # x xʸ y => (x**y)
    expr = re.sub(
        r'(\d+(\.\d+)?)\s*xʸ\s*(\d+(\.\d+)?)',
        r'(\1**\3)',
        expr
    )
    return expr

def click(event):
    global memory
    text = event.widget.cget("text")
    current = entry.get()

    if current == LIMIT_MSG and text != "C":
        entry.delete(0, tk.END)
        current = ""

    try:
        # Limit input length for all but special operations
        if text not in ["=", "C", "%", "√", "n√", "xʸ", "log", "ln", "π", "M+", "M-", "MR", "MC", "⌫", "History",
                        "sin", "cos", "tan", "(", ")", "!", "exp", "|x|"]:
            if len(current) >= MAX_INPUT_LENGTH:
                entry.delete(0, tk.END)
                entry.insert(0, LIMIT_MSG)
                return

        if text == "=":
            expr = entry.get()
            if expr == LIMIT_MSG:
                return
            expr = preprocess_expression(expr)
            try:
                allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
                allowed_names.update({"abs": abs})
                result = str(eval(expr, {"__builtins__": None}, allowed_names))
                entry.delete(0, tk.END)
                entry.insert(tk.END, result)
                update_history(expr, result)
            except Exception:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error!")
        elif text == "C":
            entry.delete(0, tk.END)
        elif text == "%":
            try:
                value = float(entry.get())
                result = value / 100
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(result))
                update_history(f"{value}%", result)
            except:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error!")
        elif text == "√":
            try:
                value = float(entry.get())
                result = math.sqrt(value)
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(result))
                update_history(f"√({value})", result)
            except:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error!")
        elif text == "n√":
            try:
                expr = entry.get()
                if not expr:
                    raise ValueError
                value = float(expr)
                n = simpledialog.askfloat("Nth Root", "Enter n (root degree):", minvalue=1)
                if n is None:
                    return
                result = value ** (1/n)
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(result))
                update_history(f"{n}√({value})", result)
            except Exception:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error!")
        elif text == "xʸ":
            try:
                expr = entry.get()
                x = float(expr)
                y = simpledialog.askfloat("Exponent", "Enter exponent (y):")
                if y is None:
                    return
                result = x ** y
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(result))
                update_history(f"{x}^{y}", result)
            except:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error!")
        elif text == "log":
            try:
                value = float(entry.get())
                result = math.log10(value)
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(result))
                update_history(f"log({value})", result)
            except:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error!")
        elif text == "ln":
            try:
                value = float(entry.get())
                result = math.log(value)
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(result))
                update_history(f"ln({value})", result)
            except:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error!")
        elif text == "π":
            if len(current) < MAX_INPUT_LENGTH:
                entry.insert(tk.END, str(math.pi))
                update_history("π", math.pi)
            else:
                entry.delete(0, tk.END)
                entry.insert(0, LIMIT_MSG)

        # --- Improved Memory Logic ---
        elif text == "M+":
            try:
                value = float(entry.get())
                memory += value
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(memory))
                update_history("M+", memory)
            except:
                pass  # Do nothing if entry is invalid
        elif text == "M-":
            try:
                value = float(entry.get())
                memory -= value
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(memory))
                update_history("M-", memory)
            except:
                pass
        elif text == "MR":
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(memory))
            update_history("MR", memory)
        elif text == "MC":
            memory = 0
            entry.delete(0, tk.END)
            entry.insert(tk.END, "0")
            update_history("MC", memory)
        # ----------------------------

        elif text == "⌫":
            if current == LIMIT_MSG:
                entry.delete(0, tk.END)
            elif current:
                entry.delete(len(current)-1, tk.END)
        elif text == "History":
            show_history()
        elif text in ("(", ")"):
            if len(current) < MAX_INPUT_LENGTH:
                entry.insert(tk.END, text)
            else:
                entry.delete(0, tk.END)
                entry.insert(0, LIMIT_MSG)
        elif text in ("sin", "cos", "tan"):
            try:
                value = float(entry.get())
                if text == "sin":
                    result = math.sin(math.radians(value))
                elif text == "cos":
                    result = math.cos(math.radians(value))
                elif text == "tan":
                    result = math.tan(math.radians(value))
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(result))
                update_history(f"{text}({value})", result)
            except:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error!")
        elif text == "!":
            try:
                value = float(entry.get())
                if value < 0 or not value.is_integer():
                    raise ValueError
                result = math.factorial(int(value))
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(result))
                update_history(f"{int(value)}!", result)
            except:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error!")
        elif text == "exp":
            try:
                value = float(entry.get())
                result = math.exp(value)
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(result))
                update_history(f"exp({value})", result)
            except:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error!")
        elif text == "|x|":
            try:
                value = float(entry.get())
                result = abs(value)
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(result))
                update_history(f"|{value}|", result)
            except:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error!")
        else:
            entry.insert(tk.END, text)
    except:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error!")

root = tk.Tk()
root.title("Calculator")
root.config(bg=BG_COLOR)

entry = tk.Entry(root, font=ENTRY_FONT, borderwidth=0, relief=tk.FLAT, justify='right',
                 bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG)
entry.grid(row=0, column=0, columnspan=6, ipadx=12, ipady=15, pady=15, padx=10, sticky="ew")

utility_buttons = ["M+", "M-", "MR", "MC", "⌫", "History"]
for j, btn_text in enumerate(utility_buttons):
    btn = tk.Button(root, text=btn_text, font=FONT, width=5, height=2,
                    bg=BTN_BG_OP, fg=BTN_FG, borderwidth=0)
    btn.grid(row=1, column=j, padx=5, pady=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.bind("<Button-1>", click)

buttons = [
    ["(", ")", "sin", "cos", "tan", "/"],
    ["7", "8", "9", "√", "xʸ", "*"],
    ["4", "5", "6", "n√", "log", "-"],
    ["1", "2", "3", "ln", "exp", "+"],
    ["0", ".", "%", "!", "C", "="],
    ["π", "|x|", "", "", "", ""],
]

for i, row in enumerate(buttons):
    for j, btn_text in enumerate(row):
        if btn_text:
            if btn_text.isdigit() or btn_text == ".":
                bg_color = BTN_BG_NUM
            elif btn_text in ["+", "-", "*", "/", "=", "⌫"]:
                bg_color = BTN_BG_OP
            else:
                bg_color = BTN_BG_FUNC

            btn = tk.Button(root, text=btn_text, font=FONT, width=5, height=2,
                            bg=bg_color, fg=BTN_FG, borderwidth=0)
            btn.grid(row=i+2, column=j, padx=5, pady=5)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            btn.bind("<Button-1>", click)

root.mainloop()
