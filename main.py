import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Set the main window
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welcome to Home Eats Restaurant")
        self.geometry("500x450")

        self.cart = []

        # add restaurant image
        self.image = Image.open("image/interior1.png").resize((400, 200))
        self.photo = ImageTk.PhotoImage(self.image)
        tk.Label(self, image=self.photo).pack(pady=5)

        # add labels
        tk.Label(self, text="Welcome to Home Eats Online Ordering", font=("Arial", 18)).pack(pady=10)
        tk.Label(self, text="Authentic Chinese Cuisine!", font=("Arial", 12)).pack(pady=5)

        # add button to navigate through windows
        tk.Button(self, text="View Menu", command=self.open_menu_window).pack(pady=5)
        tk.Button(self, text="My Cart", command=self.open_cart_window).pack(pady=5)
        tk.Button(self, text="Exit", command=self.quit).pack(pady=5)
    
    #set menu and cart button handler
    def open_menu_window(self):
        MenuWindow(self)

    def open_cart_window(self):
        CartWindow(self)


# Set the menu window layout:title, backgroud color,size
class MenuWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Menu")
        self.geometry("800x520")
        self.configure(bg="#333333")
        
        # put all the menu information as a list of dictionaries
        self.menu_items = [
            {"name": "Boiled Spicy Fish", "price": 32, "image": "image/boiled_spicy_fish.jpeg"},
            {"name": "Spicy Crayfish", "price": 19.95, "image": "image/crayfish.jpeg"},
            {"name": "Sweet and Sour Pine Nut Fish", "price": 35, "image": "image/sweet_and_sour_pine_nut_fish.jpeg"},
            {"name": "Steamed Oysters with Garlic Sauce", "price": 36, "image": "image/oyster.jpeg"},
            {"name": "Stir-Fried Chicken with Peppers", "price": 32, "image": "image/stir_fried_chicken_with_Peppers.jpeg"},
            {"name": "Stir-Fried Beef", "price": 28, "image": "image/stir_fried_beef.jpeg"},
            {"name": "Preserved Quail Eggs", "price": 16, "image": "image/preserved_quail_eggs.jpeg"},
            {"name": "Steamed Pork Belly ", "price": 22, "image": "image/steamed_pork_belly.jpeg"}
        ]

        # set the menu layout, four each row has four items
        for index, item in enumerate(self.menu_items):
            row = index // 4
            col = index % 4

            #each menu has one image, a title, a price and an add to cart button
            img = Image.open(item["image"]).resize((150, 100))
            photo = ImageTk.PhotoImage(img)

            lbl_image = tk.Label(self, image=photo, bg="#000000")
            lbl_image.image = photo
            lbl_image.grid(row=row * 3, column=col, padx=20, pady=25)

            lbl_text = tk.Label(
                self,
                text=f"{item['name']}\n${item['price']}",
                font=("Helvetica", 11),
                fg="#FFFFFF"
            )
            lbl_text.grid(row=row * 3 + 1, column=col)

            btn_add = tk.Button(
                 self,
                text="Add to Cart",
                command=lambda i=item: self.add_to_cart(i),
                font=("Helvetica", 8),
                fg="#000000",  # 按钮字体颜色
                relief="flat",  # 去除按钮边框样式
                highlightthickness=0 
            )
            btn_add.grid(row=row * 3 + 2, column=col, pady=5)

          
        #add a button to navigate back to main window
        tk.Button(self, text="Back to Homepage", command=self.close_menu, fg="black").grid(
            row=len(self.menu_items) // 4 * 3 + 2, column=0, columnspan=4, pady=20
        )
        #add a button to navigate back to cart
        tk.Button(self, text="Go to cart", command=self.go_to_cart, fg="black").grid(
            row=len(self.menu_items) // 4 * 3 + 1, column=0, columnspan=4, pady=10
        )
    #set the add_to_cart button handler
    def add_to_cart(self, item):
        for cart_item in self.master.cart:
            if cart_item["name"] == item["name"]:
                cart_item["quantity"] += 1
                break
        else:
            self.master.cart.append({"name": item["name"], "price": item["price"], "quantity": 1})
        print(f"{item['name']} has been added to the cart!")
    
    
    #set the go_to_cart button handler
    def go_to_cart(self):
        CartWindow(self.master)

    #set the "Back to Homepage"  button handler
    def close_menu(self):
        self.destroy()


# set the cart window
class CartWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("My Cart")
        self.geometry("400x500")
        self.configure(bg="#333333") 

        # 
        self.cart_items = master.cart if hasattr(master, 'cart') else []  
        self.total_price = tk.DoubleVar(value=self.calculate_total())

        # add the lable as the title 
        tk.Label(self, text="Shopping Cart", font=("Helvetica", 14), bg="#333333", fg="white").pack(pady=10)

        # Add a listbox to display the cart items 
        self.cart_listbox = tk.Listbox(self, width=45, height=10, bg="#333333", fg="white", highlightthickness=0, borderwidth=0)
        self.cart_listbox.pack(pady=10)
        self.update_cart_display()

        # show the total bill price
        tk.Label(self, text="Total Price:", font=("Helvetica", 12), bg="#333333", fg="white").pack()
        self.total_label = tk.Label(self, textvariable=self.total_price, font=("Helvetica", 12), bg="#333333", fg="white")
        self.total_label.pack()

        # set the buttons
        tk.Button(self, text="Remove Selected", command=self.remove_selected, bg="white", fg="black", relief="flat").pack(pady=5)
        tk.Button(self, text="Clear Cart", command=self.clear_cart, bg="white", fg="black", relief="flat").pack(pady=5)
        tk.Button(self, text="Submit Order", command=self.submit_order, bg="white", fg="black", relief="flat").pack(pady=10)
    
    #Update the listbox to show the current items in the cart
    def update_cart_display(self):
        self.cart_listbox.delete(0, tk.END)
        for item in self.cart_items:
            self.cart_listbox.insert(tk.END, f"{item['name']} x {item['quantity']} - ${item['price'] * item['quantity']:.2f}")
    
    #Calculate the total price of all items in the cart
    def calculate_total(self):
        return sum(item['price'] * item['quantity'] for item in self.cart_items)

    #Remove the selected item from the cart
    def remove_selected(self):
        selected_index = self.cart_listbox.curselection()
        if selected_index:
            del self.cart_items[selected_index[0]]
            self.update_cart_display()
            self.total_price.set(self.calculate_total())
    
    #clear the cart content
    def clear_cart(self):
        self.cart_items.clear()
        self.update_cart_display()
        self.total_price.set(0)

    #submit the order and clear the cart
    def submit_order(self):
        if not self.cart_items:
            tk.messagebox.showinfo("Cart Empty", "Your cart is empty. Add items before submitting.")
            return
        tk.messagebox.showinfo("Order Submitted", "Your order has been submitted successfully!")
        self.clear_cart()  


#start the program
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
