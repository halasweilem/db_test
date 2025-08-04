import sqlite3

conn = sqlite3.connect('bankk_database.db')
print("Database connected successfully.")

cursor = conn.cursor()

# Create 'customers' table (parent)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
''')
print("Customers table created successfully.")

# Insert some customers
cursor.execute("INSERT INTO customers (name, age) VALUES ('Hala Sweilem', 21)")
cursor.execute("INSERT INTO customers (name, age) VALUES ('Sarah Ateya', 35)")
conn.commit()
print("Customers inserted successfully.")

# Create 'accounts' table (child) with foreign key referencing customers.customer_id
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        account_type TEXT NOT NULL,
        balance REAL NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    )
''')
conn.commit()
print("Accounts table created successfully.")

# Insert accounts referencing customers by customer_id
cursor.execute("INSERT INTO accounts (customer_id, account_type, balance) VALUES (1, 'Checking', 150.00)")
cursor.execute("INSERT INTO accounts (customer_id, account_type, balance) VALUES (1, 'Savings', 500.00)")
cursor.execute("INSERT INTO accounts (customer_id, account_type, balance) VALUES (2, 'Checking', 3000.00)")
conn.commit()
print("Accounts inserted successfully.")

# Query to join customers with their accounts
cursor.execute('''
    SELECT customers.name, accounts.account_type, accounts.balance
    FROM accounts
    JOIN customers ON accounts.customer_id = customers.customer_id
''')

rows = cursor.fetchall()
print("\nCustomer Accounts:")
for row in rows:
    print(f"Customer: {row[0]}, Account Type: {row[1]}, Balance: ${row[2]:.2f}")

conn.close()
print("Database connection closed.")