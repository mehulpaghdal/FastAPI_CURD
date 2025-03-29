# =============================mysql=============================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error

app = FastAPI()

origins = ["*"]  # Change the allowed origins as needed.
# middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create a connection to the database
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="",
            username="root",
            password=""
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


#
# Get all records
@app.get("/records")
async def read_records():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usermaster")
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    return records


# Get a single record by ID
@app.get("/records/{record_id}")
async def read_record(record_id: int):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM usermaster WHERE id = {record_id}")
    record = cursor.fetchone()
    cursor.close()
    connection.close()
    return record


# Create a new record
@app.post("/records")
async def create_record(name: str, email: str, password: str):
    connection = create_connection()
    cursor = connection.cursor()
    # cursor.execute("INSERT INTO usermaster (name, email ,password) VALUES (%s, %s, %s)", (name, email, password))
    q = f"insert into usermaster (name, email, password) VALUES ('{name}','{email}','{password}')"
    print(q)
    cursor.execute(q)
    connection.commit()
    record_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return {"id": record_id, "name": name, "email": email, "password": password}


# Update a record by ID
@app.put("/records/{record_id}")
async def update_record(record_id: int, name: str, email: str, password: str):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE usermaster SET name = %s, email = %s, password= %s WHERE id = %s",
                   (name, email, password, record_id))
    connection.commit()
    updated_rows = cursor.rowcount
    cursor.close()
    connection.close()
    if updated_rows == 0:
        return {"error": "Record not found"}
    else:
        return {"id": record_id, "name": name, "email": email, "password": password}


# Delete a record by ID
@app.delete("/records/{record_id}")
async def delete_record(record_id: int):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM usermaster WHERE id = %s", (record_id,))
    connection.commit()
    deleted_rows = cursor.rowcount
    cursor.close()
    connection.close()
    if deleted_rows == 0:
        return {"error": "Record not found"}
    else:
        return {"message": "Record deleted successfully"}

# ============================================MSSQL=============================
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import pyodbc
#
#
# class Item(BaseModel):
#     name: str
#     price: float
#
#
# app = FastAPI()
# conn = pyodbc.connect(
#     "Driver={ODBC Driver 17 for SQL Server};"
#     "Server=CS_T0512;"
#     "Database=db_icons;"
#     "Trusted_Connection=yes;"
# )
# cursor = conn.cursor()
#
#
# @app.post("/items/")
# async def create_item(item: Item):
#     query = f"INSERT INTO tbl_usermaster (name, price) VALUES (?, ?)"
#     values = (item.name, item.price)
#     cursor.execute(query, values)
#     conn.commit()
#     return {"message": "Item created successfully"}
#
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     query = f"SELECT * FROM tbl_usermaster WHERE id = {item_id}"
#     cursor.execute(query)
#     row = cursor.fetchone()
#     if not row:
#         raise HTTPException(status_code=404, detail="Item not found")
#     item = {"id": row[0], "name": row[1], "price": row[2]}
#     return item
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     query = f"UPDATE items SET name = ?, price = ? WHERE id = {item_id}"
#     values = (item.name, item.price)
#     cursor.execute(query, values)
#     conn.commit()
#     return {"message": "Item updated successfully"}
#
#
# @app.delete("/items/{item_id}")
# async def delete_item(item_id: int):
#     query = f"DELETE FROM items WHERE id = {item_id}"
#     cursor.execute(query)
#     conn.commit()
#     return {"message": "Item deleted successfully"}
#
#
# @app.get("/items/")
# async def read_items():
#     query = "SELECT * FROM tbl_usermaster"
#     cursor.execute(query)
#     rows = cursor.fetchall()
#     items = []
#     for row in rows:
#         item = {"id": row[0], "name": row[1], "price": row[2]}
#         items.append(item)
#     return items

