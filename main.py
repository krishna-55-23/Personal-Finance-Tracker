
import tkinter as tk
from app import FinanceTrackerApp
from ui import styles

def main():
    root = tk.Tk()
    styles.apply_styles(root)  # Apply modern styles
    app = FinanceTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
