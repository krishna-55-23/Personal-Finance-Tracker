
import sqlite3
from datetime import datetime

def create_connection():
    """Create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect('C:/Users/KRISHNA/personal_finance_tracker/finance.db')
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(conn):
    """Create table"""
    try:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                note TEXT
            );
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS budget (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month TEXT NOT NULL UNIQUE,
                amount REAL NOT NULL
            );
        """)
    except sqlite3.Error as e:
        print(e)

def add_transaction(conn, transaction):
    """Add a new transaction to the transactions table"""
    sql = ''' INSERT INTO transactions(type,amount,category,date,note)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, transaction)
    conn.commit()
    return cur.lastrowid

def get_transactions(conn, month=None):
    """Query all rows in the transactions table"""
    cur = conn.cursor()
    if month:
        cur.execute("SELECT * FROM transactions WHERE strftime('%Y-%m', date) = ?", (month,))
    else:
        cur.execute("SELECT * FROM transactions")
    rows = cur.fetchall()
    return rows

def get_budget(conn, month):
    """Query budget for a specific month"""
    cur = conn.cursor()
    cur.execute("SELECT amount FROM budget WHERE month=?", (month,))
    row = cur.fetchone()
    return row[0] if row else 0

def set_budget(conn, month, amount):
    """Set budget for a specific month"""
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO budget (month, amount) VALUES (?, ?)", (month, amount))
    conn.commit()

def init_database():
    from database import create_connection, init_database, add_transaction, get_transactions

# Step 1: Initialize DB
init_database()

# Step 2: Connect to database
conn = create_connection()

# Step 3: Add a transaction
transaction = (
    "expense",            # type
    500,                  # amount
    "Groceries",          # category
    "2025-08-08",         # date
    "Bought vegetables"   # note
)
add_transaction(conn, transaction)

# Step 4: Fetch transactions
transactions = get_transactions(conn)
for t in transactions:
    print(t)

# Step 5: Close connection
conn.close()

if __name__ == "__main__":
    init_database()
    conn = create_connection()

    # Example: Add test transaction
    add_transaction(conn, ("income", 1000, "Salary", "2025-08-08", "August salary"))

    # Example: Fetch all
    for row in get_transactions(conn):
        print(row)

    conn.close()

    
"""    conn = create_connection()
    if conn is not None:
        create_table(conn)
        conn.close()
"""