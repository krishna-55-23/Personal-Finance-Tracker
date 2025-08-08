
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

import database

class FinanceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("800x600")

        self.conn = database.create_connection()
        database.create_table(self.conn)

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Add Transaction")
        input_frame.pack(fill=tk.X, pady=10)

        ttk.Label(input_frame, text="Type:").grid(row=0, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar(value="Expense")
        ttk.Combobox(input_frame, textvariable=self.type_var, values=["Expense", "Income"]).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.category_entry = ttk.Combobox(input_frame, values=["Food", "Transport", "Bills", "Shopping", "Income"])
        self.category_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Date:").grid(row=3, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(input_frame, text="Note:").grid(row=4, column=0, padx=5, pady=5)
        self.note_entry = ttk.Entry(input_frame)
        self.note_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="Add", command=self.add_transaction).grid(row=5, column=0, columnspan=2, pady=10)

        # History frame
        history_frame = ttk.LabelFrame(main_frame, text="Transaction History")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree = ttk.Treeview(history_frame, columns=("ID", "Type", "Amount", "Category", "Date", "Note"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        self.load_transactions()

        # Summary frame
        summary_frame = ttk.LabelFrame(main_frame, text="Summary")
        summary_frame.pack(fill=tk.X, pady=10)

        ttk.Button(summary_frame, text="Show Monthly Summary", command=self.show_summary).pack(side=tk.LEFT, padx=5)
        ttk.Button(summary_frame, text="Export to CSV", command=self.export_to_csv).pack(side=tk.LEFT, padx=5)

        # Budget frame
        budget_frame = ttk.LabelFrame(main_frame, text="Budget")
        budget_frame.pack(fill=tk.X, pady=10)

        ttk.Label(budget_frame, text="Month (YYYY-MM):").pack(side=tk.LEFT, padx=5)
        self.budget_month_entry = ttk.Entry(budget_frame)
        self.budget_month_entry.pack(side=tk.LEFT, padx=5)
        self.budget_month_entry.insert(0, datetime.now().strftime("%Y-%m"))

        ttk.Label(budget_frame, text="Amount:").pack(side=tk.LEFT, padx=5)
        self.budget_amount_entry = ttk.Entry(budget_frame)
        self.budget_amount_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(budget_frame, text="Set Budget", command=self.set_budget).pack(side=tk.LEFT, padx=5)

    def add_transaction(self):
        try:
            type = self.type_var.get()
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            date = self.date_entry.get()
            note = self.note_entry.get()

            if not all([type, amount, category, date]):
                messagebox.showerror("Error", "Please fill all fields.")
                return

            transaction = (type, amount, category, date, note)
            database.add_transaction(self.conn, transaction)
            self.load_transactions()
            self.check_budget()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")

    def load_transactions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        rows = database.get_transactions(self.conn)
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def show_summary(self):
        month = self.budget_month_entry.get()
        rows = database.get_transactions(self.conn, month)

        if not rows:
            messagebox.showinfo("Info", f"No transactions for {month}")
            return

        expenses = { }
        total_income = 0
        total_expense = 0

        for row in rows:
            type, amount, category = row[1], row[2], row[3]
            if type == "Expense":
                total_expense += amount
                expenses[category] = expenses.get(category, 0) + amount
            else:
                total_income += amount

        self.plot_pie_chart(expenses)

    def plot_pie_chart(self, expenses):
        if not expenses:
            return

        labels = expenses.keys()
        sizes = expenses.values()

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        chart_window = tk.Toplevel(self.root)
        chart_window.title("Expense Distribution")
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def set_budget(self):
        month = self.budget_month_entry.get()
        try:
            amount = float(self.budget_amount_entry.get())
            database.set_budget(self.conn, month, amount)
            messagebox.showinfo("Success", f"Budget for {month} set to {amount}")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")

    def check_budget(self):
        month = datetime.now().strftime("%Y-%m")
        budget = database.get_budget(self.conn, month)
        if budget > 0:
            rows = database.get_transactions(self.conn, month)
            total_expense = sum(row[2] for row in rows if row[1] == "Expense")
            if total_expense > budget:
                messagebox.showwarning("Budget Alert", f"You have exceeded your budget for {month}!")

    def export_to_csv(self):
        rows = database.get_transactions(self.conn)
        with open("transactions.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Type", "Amount", "Category", "Date", "Note"])
            writer.writerows(rows)
        messagebox.showinfo("Success", "Transactions exported to transactions.csv")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTrackerApp(root)
    root.mainloop()
