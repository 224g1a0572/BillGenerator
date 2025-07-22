import sqlite3

conn = sqlite3.connect('bill.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    phone TEXT,
    table_no TEXT,
    item TEXT,
    price REAL,
    qty INTEGER,
    amount REAL
)''')

conn.commit()
conn.close()
print("Database and table created.")
