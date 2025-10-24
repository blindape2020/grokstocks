import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import json
import random

class HypeDrivenStockSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Hype-Driven Stock Simulator")
        
        # Sample data based on the PNG
        self.data = [
            {"rank": 1, "name": "Tesla", "promo": "World Domination!", "weight": 20, "price": 991.00, "shares": 900000000, "market_cap": 891900000000.00, "hype_score": 55},
        ]

        # Sort by Price descending initially
        self.sort_by_price_desc()

        # Create Treeview with columns from PNG
        columns = ("Rank", "Name", "Promo Content", "Weight (chars)", "Price", "Shares Outstanding", "Market Cap", "Hype Score")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Populate table
        self.populate_table()

        # Bind right-click event
        self.tree.bind("<Button-3>", self.show_context_menu)

        # Create context menu for edits and new entry
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Edit Name", command=self.edit_name)
        self.context_menu.add_command(label="Edit Promo", command=self.edit_promo)
        self.context_menu.add_command(label="Edit Price", command=self.edit_price)
        self.context_menu.add_command(label="Edit Shares", command=self.edit_shares)
        self.context_menu.add_command(label="Edit Hype Score", command=self.edit_hype_score)
        self.context_menu.add_command(label="Add New Entry", command=self.add_new_entry_context)

        # Menu bar
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New File", command=self.new_file)
        filemenu.add_command(label="Load File", command=self.load_file)
        filemenu.add_command(label="Save File", command=self.save_file)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)

        # Buttons frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        self.simulate_button = tk.Button(button_frame, text="Simulate a Market Day", command=self.simulate_market_day)
        self.simulate_button.pack(side=tk.LEFT, padx=5)
        self.new_entry_button = tk.Button(button_frame, text="New Entry", command=self.add_new_entry_button)
        self.new_entry_button.pack(side=tk.LEFT, padx=5)

    def populate_table(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert data
        for index, row in enumerate(self.data):
            values = (
                row["rank"], row["name"], row["promo"], row["weight"], 
                f"${row['price']:.2f}", row["shares"], f"${row['market_cap']:.2f}", row["hype_score"]
            )
            self.tree.insert("", "end", iid=index, values=values)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.selected_item = item
            self.context_menu.post(event.x_root, event.y_root)

    def update_market_cap(self, index):
        row = self.data[index]
        row["market_cap"] = row["price"] * row["shares"]

    def edit_name(self):
        if hasattr(self, 'selected_item'):
            index = int(self.selected_item)
            new_value = simpledialog.askstring("Edit Name", "Enter new name:", initialvalue=self.data[index]["name"], parent=self.root)
            if new_value:
                self.data[index]["name"] = new_value
                self.populate_table()

    def edit_promo(self):
        if hasattr(self, 'selected_item'):
            index = int(self.selected_item)
            new_value = simpledialog.askstring("Edit Promo", "Enter new promo content:", initialvalue=self.data[index]["promo"], parent=self.root)
            if new_value is not None:
                self.data[index]["promo"] = new_value
                self.data[index]["weight"] = len(new_value)
                self.populate_table()

    def edit_price(self):
        if hasattr(self, 'selected_item'):
            index = int(self.selected_item)
            new_value = simpledialog.askfloat("Edit Price", "Enter new price:", initialvalue=self.data[index]["price"], parent=self.root)
            if new_value is not None:
                self.data[index]["price"] = new_value
                self.update_market_cap(index)
                self.populate_table()

    def edit_shares(self):
        if hasattr(self, 'selected_item'):
            index = int(self.selected_item)
            new_value = simpledialog.askinteger("Edit Shares", "Enter new shares outstanding:", initialvalue=self.data[index]["shares"], parent=self.root)
            if new_value is not None:
                self.data[index]["shares"] = new_value
                self.update_market_cap(index)
                self.populate_table()

    def edit_hype_score(self):
        if hasattr(self, 'selected_item'):
            index = int(self.selected_item)
            new_value = simpledialog.askinteger("Edit Hype Score", "Enter new hype score:", initialvalue=self.data[index]["hype_score"], parent=self.root)
            if new_value is not None:
                self.data[index]["hype_score"] = new_value
                self.populate_table()

    def simulate_market_day(self):
        for row in self.data:
            hype = row["hype_score"]
            if hype < 30:
                change_pct = random.uniform(-1, 1)
            elif hype <= 70:
                change_pct = random.uniform(6, 30)
            else:
                change_pct = random.uniform(-30, -10)
            
            row["price"] *= (1 + change_pct / 100)
            if row["price"] < 0:
                row["price"] = 0
            self.update_market_cap(self.data.index(row))
        
        self.sort_by_price_desc()
        self.populate_table()
        messagebox.showinfo("Simulation Complete", "Market day simulated! Prices updated based on hype factors.")

    def sort_by_price_desc(self):
        self.data.sort(key=lambda x: x["price"], reverse=True)
        for i, row in enumerate(self.data, start=1):
            row["rank"] = i

    def new_file(self):
        if messagebox.askyesno("New File", "Are you sure? This will clear current data."):
            self.data = []
            self.populate_table()

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                self.data = json.load(file)
            self.sort_by_price_desc()
            self.populate_table()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.data, file, indent=4)
            messagebox.showinfo("Save Successful", f"Data saved to {file_path}")

    def add_new_entry_context(self):
        new_entry = {
            "rank": len(self.data) + 1,
            "name": "New Stock",
            "promo": "",
            "weight": 0,
            "price": 100.00,
            "shares": 1000000,
            "market_cap": 100000000.00,
            "hype_score": 50
        }
        self.data.append(new_entry)
        self.sort_by_price_desc()
        self.populate_table()

    def add_new_entry_button(self):
        new_entry = {
            "rank": len(self.data) + 1,
            "name": "New Stock",
            "promo": "",
            "weight": 0,
            "price": 100.00,
            "shares": 1000000,
            "market_cap": 100000000.00,
            "hype_score": 50
        }
        self.data.append(new_entry)
        self.sort_by_price_desc()
        self.populate_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = HypeDrivenStockSimulator(root)
    root.mainloop()