from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running. Please open http://127.0.0.1:8000/docs to proceed."}

DB_NAME = "bankk_database.db"

# Pydantic models
class Customer(BaseModel):
    name: str
    age: int

class UpdateCustomer(BaseModel):
    name: str = None
    age: int = None

# Class to manage DB operations
class BankAPI:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def insert_customer(self, customer: Customer):
        self.cursor.execute(
            "INSERT INTO customers (name, age) VALUES (?, ?)",
            (customer.name, customer.age),
        )
        self.conn.commit()
        return {"message": "Customer added successfully"}

    def get_customers(self):
        self.cursor.execute("SELECT * FROM customers")
        rows = self.cursor.fetchall()
        return rows

    def update_customer(self, customer_id: int, customer: UpdateCustomer):
        if customer.name:
            self.cursor.execute(
                "UPDATE customers SET name = ? WHERE customer_id = ?",
                (customer.name, customer_id),
            )
        if customer.age:
            self.cursor.execute(
                "UPDATE customers SET age = ? WHERE customer_id = ?",
                (customer.age, customer_id),
            )
        self.conn.commit()
        return {"message": "Customer updated"}

    def delete_customer(self, customer_id: int):
        self.cursor.execute("DELETE FROM customers WHERE customer_id = ?", (customer_id,))
        self.conn.commit()
        return {"message": "Customer deleted"}


db = BankAPI()

# FastAPI routes
@app.post("/customers/")
def create_customer(customer: Customer):
    return db.insert_customer(customer)

@app.get("/customers/")
def read_customers():
    return db.get_customers()

@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: UpdateCustomer):
    return db.update_customer(customer_id, customer)

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    return db.delete_customer(customer_id)

