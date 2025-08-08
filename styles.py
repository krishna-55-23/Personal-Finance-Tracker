
from tkinter import ttk

def apply_styles(root):
    style = ttk.Style(root)
    style.theme_use('clam')

    # Configure styles for widgets
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
    style.configure("TButton", font=("Arial", 10, "bold"), foreground="white", background="#4CAF50")
    style.map("TButton", background=[('active', '#45a049')])
    style.configure("TEntry", font=("Arial", 10), padding=5)
    style.configure("TCombobox", font=("Arial", 10), padding=5)
    style.configure("Treeview", font=("Arial", 10), rowheight=25)
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    style.configure("TLabelFrame", font=("Arial", 12, "bold"), borderwidth=2, relief="groove")
    style.configure("TLabelFrame.Label", font=("Arial", 12, "bold"), background="#f0f0f0")
