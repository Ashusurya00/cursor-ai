import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        
        # Calculator state
        self.current_number = ""
        self.first_number = 0
        self.operation = ""
        self.should_reset = False
        
        # Create display
        self.create_display()
        
        # Create buttons
        self.create_buttons()
        
        # Style configuration
        self.style_buttons()
    
    def create_display(self):
        # Display frame
        display_frame = tk.Frame(self.root, bg="#2c3e50", height=120)
        display_frame.pack(fill="x", padx=10, pady=10)
        display_frame.pack_propagate(False)
        
        # Display label
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        self.display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 32, "bold"),
            bg="#34495e",
            fg="white",
            anchor="e",
            padx=20,
            pady=20
        )
        self.display.pack(fill="both", expand=True)
    
    def create_buttons(self):
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#2c3e50")
        buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid weights
        for i in range(6):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Button definitions
        button_data = [
            ("C", 0, 0, "#e74c3c"), ("±", 0, 1, "#95a5a6"), ("%", 0, 2, "#95a5a6"), ("÷", 0, 3, "#f39c12"),
            ("7", 1, 0, "#34495e"), ("8", 1, 1, "#34495e"), ("9", 1, 2, "#34495e"), ("×", 1, 3, "#f39c12"),
            ("4", 2, 0, "#34495e"), ("5", 2, 1, "#34495e"), ("6", 2, 2, "#34495e"), ("-", 2, 3, "#f39c12"),
            ("1", 3, 0, "#34495e"), ("2", 3, 1, "#34495e"), ("3", 3, 2, "#34495e"), ("+", 3, 3, "#f39c12"),
            ("0", 4, 0, "#34495e", 2), (".", 4, 2, "#34495e"), ("=", 4, 3, "#f39c12"),
            ("√", 5, 0, "#9b59b6"), ("x²", 5, 1, "#9b59b6"), ("1/x", 5, 2, "#9b59b6"), ("⌫", 5, 3, "#e67e22")
        ]
        
        # Create buttons
        self.buttons = {}
        for data in button_data:
            if len(data) == 5:  # Button with colspan
                text, row, col, color, colspan = data
                button = tk.Button(
                    buttons_frame,
                    text=text,
                    font=("Arial", 18, "bold"),
                    bg=color,
                    fg="white",
                    relief="flat",
                    command=lambda t=text: self.button_click(t)
                )
                button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)
            else:
                text, row, col, color = data
                button = tk.Button(
                    buttons_frame,
                    text=text,
                    font=("Arial", 18, "bold"),
                    bg=color,
                    fg="white",
                    relief="flat",
                    command=lambda t=text: self.button_click(t)
                )
                button.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            
            self.buttons[text] = button
    
    def style_buttons(self):
        # Add hover effects
        for button in self.buttons.values():
            button.bind("<Enter>", lambda e, b=button: self.on_hover(b, True))
            button.bind("<Leave>", lambda e, b=button: self.on_hover(b, False))
    
    def on_hover(self, button, entering):
        if entering:
            # Darken the button
            current_color = button.cget("bg")
            if current_color == "#34495e":
                button.configure(bg="#2c3e50")
            elif current_color == "#f39c12":
                button.configure(bg="#e67e22")
            elif current_color == "#e74c3c":
                button.configure(bg="#c0392b")
            elif current_color == "#95a5a6":
                button.configure(bg="#7f8c8d")
            elif current_color == "#9b59b6":
                button.configure(bg="#8e44ad")
            elif current_color == "#e67e22":
                button.configure(bg="#d35400")
        else:
            # Restore original color
            button.configure(bg=button.master.children[button.winfo_name()]["bg"])
    
    def button_click(self, value):
        if value.isdigit() or value == ".":
            self.handle_number(value)
        elif value in ["+", "-", "×", "÷"]:
            self.handle_operator(value)
        elif value == "=":
            self.calculate()
        elif value == "C":
            self.clear()
        elif value == "±":
            self.toggle_sign()
        elif value == "%":
            self.percentage()
        elif value == "√":
            self.square_root()
        elif value == "x²":
            self.square()
        elif value == "1/x":
            self.reciprocal()
        elif value == "⌫":
            self.backspace()
    
    def handle_number(self, number):
        if self.should_reset:
            self.current_number = ""
            self.should_reset = False
        
        if number == "." and "." in self.current_number:
            return
        
        self.current_number += number
        self.update_display()
    
    def handle_operator(self, operator):
        if self.current_number:
            if self.operation and not self.should_reset:
                self.calculate()
            
            self.first_number = float(self.current_number)
            self.operation = operator
            self.should_reset = True
        elif self.operation and self.should_reset:
            self.operation = operator
    
    def calculate(self):
        if not self.current_number or not self.operation:
            return
        
        second_number = float(self.current_number)
        result = 0
        
        if self.operation == "+":
            result = self.first_number + second_number
        elif self.operation == "-":
            result = self.first_number - second_number
        elif self.operation == "×":
            result = self.first_number * second_number
        elif self.operation == "÷":
            if second_number == 0:
                self.display_var.set("Error")
                return
            result = self.first_number / second_number
        
        # Format result
        if result.is_integer():
            result = int(result)
        
        self.display_var.set(str(result))
        self.current_number = str(result)
        self.operation = ""
        self.should_reset = True
    
    def clear(self):
        self.current_number = ""
        self.first_number = 0
        self.operation = ""
        self.should_reset = False
        self.display_var.set("0")
    
    def toggle_sign(self):
        if self.current_number:
            if self.current_number.startswith("-"):
                self.current_number = self.current_number[1:]
            else:
                self.current_number = "-" + self.current_number
            self.update_display()
    
    def percentage(self):
        if self.current_number:
            result = float(self.current_number) / 100
            if result.is_integer():
                result = int(result)
            self.current_number = str(result)
            self.update_display()
    
    def square_root(self):
        if self.current_number:
            number = float(self.current_number)
            if number < 0:
                self.display_var.set("Error")
                return
            result = math.sqrt(number)
            if result.is_integer():
                result = int(result)
            self.current_number = str(result)
            self.update_display()
    
    def square(self):
        if self.current_number:
            result = float(self.current_number) ** 2
            if result.is_integer():
                result = int(result)
            self.current_number = str(result)
            self.update_display()
    
    def reciprocal(self):
        if self.current_number:
            number = float(self.current_number)
            if number == 0:
                self.display_var.set("Error")
                return
            result = 1 / number
            if result.is_integer():
                result = int(result)
            self.current_number = str(result)
            self.update_display()
    
    def backspace(self):
        if self.current_number:
            self.current_number = self.current_number[:-1]
            if not self.current_number:
                self.current_number = "0"
            self.update_display()
    
    def update_display(self):
        if not self.current_number:
            self.display_var.set("0")
        else:
            self.display_var.set(self.current_number)

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 