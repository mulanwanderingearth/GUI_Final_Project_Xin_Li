import tkinter as tk
from tkinter import messagebox

# Main Window
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welcome to Home Eats Resterant")
        self.geometry("400x300")

        # Labels
        tk.Label(self, text="Welcome to Home Eats", font=("Arial", 18)).pack(pady=10)
        tk.Label(self, text="Best Sichuan Cuisine in Town!", font=("Arial", 12)).pack(pady=5)
        tk.Label(self, text="Choose an option to get started:", font=("Arial", 10)).pack(pady=5)

        # Buttons
        tk.Button(self, text="View Menu", command=self.open_menu_window).pack(pady=5)
        tk.Button(self, text="My Cart", command=self.open_cart_window).pack(pady=5)
        tk.Button(self, text="Exit", command=self.quit).pack(pady=5)

    def open_menu_window(self):
        MenuWindow(self)

    def open_cart_window(self):
        CartWindow(self)


# Menu Window
class MenuWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Menu")
        self.geometry("400x300")
        self.menu_items = {"Mapo Tofu": 12, "Kung Pao Chicken": 15, "Hot and Sour Soup": 8}

        tk.Label(self, text="Menu", font=("Arial", 16)).pack(pady=10)
        for item, price in self.menu_items.items():
            tk.Button(self, text=f"{item} - ${price}", command=lambda i=item: self.add_to_cart(i)).pack(pady=5)

        tk.Button(self, text="Back to Main", command=self.destroy).pack(pady=10)

    def add_to_cart(self, item):
        # Add item to cart 
        messagebox.showinfo("Added to Cart", f"{item} has been added to your cart!")


# Cart Window (Placeholder)
class CartWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("My Cart")
        tk.Label(self, text="Cart Window (Coming Soon)").pack()


# Run the Application
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

