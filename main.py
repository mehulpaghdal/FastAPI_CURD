import pyodbc
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    number: str
    city: str
    salary: int


class Fullitem(Item):
    id: int


app = FastAPI()


def create_connection():
    try:
        connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                    'Server=ENTER SEVER;'
                                    'Database=ENTER DATABASE NAME;'
                                    'Trusted_Connection=yes;')
        cursor = connection.cursor()
        if cursor:
            print("connected successfully....")
        else:
            print("No cursor available")
        return connection

    except Exception as e:
        return HTTPException(status_code=500, detail="Database connection error...")


def resultset(cursor):
    sets = []
    while True:
        names = [c[0] for c in cursor.description]
        set_ = []
        while True:
            row_data = cursor.fetchone()
            if row_data is None:
                break
            row = dict(zip(names, row_data))
            set_.append(row)
        sets.append(list(set_))
        if cursor.nextset() is None or cursor.description is None:
            break
    return sets


@app.get("/records/")
async def get_data():
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("select * from data")
        data = resultset(cur)
        return {
            "code": 200,
            "message": "success",
            "details": data[0]
        }
    except pyodbc.Error as e:
        print(f"Error while fetch records...{e}")
        raise HTTPException(status_code=404, detail="Failed to fetch records")


@app.get("/records/{id}")
async def get_id_data(id: int):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("select * from data where id = ?", id)
        data_id = resultset(cur)
        return {
            "code": 200,
            "message": "success",
            "details": data_id
        }
    except pyodbc.Error as e:
        print(f"Error while fetching record id...{e}")
        raise HTTPException(status_code=404, detail="Failed to fetch record id")


@app.post("/add_data/")
# async def create_new_data(item: Item):
async def create_new_data(fullitem: Fullitem):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("insert into data(Id, Name, Number, City, Salary) values (?,?,?,?,?)",
                    (fullitem.id, fullitem.name, fullitem.number, fullitem.city, fullitem.salary))
        conn.commit()
        return {
            "code": 200,
            "message": "success",
            "details": "New data created successfully..."
        }
    except pyodbc.Error as e:
        print(f"Error while creating new records...{e}")
        raise HTTPException(status_code=404, detail="Failed to create new records")


@app.put("/update_data/{id}")
async def update_details(id: int, item: Item):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("update data set Name=?, Number=?, City=?, Salary=? where ID = ?",
                    (item.name, item.number, item.city, item.salary, id))
        conn.commit()
        return {
            "code": 200,
            "message": "success",
            "details": "data updated successfully"
        }
    except pyodbc.Error as e:
        print(f"Error while updating records...{e}")
        raise HTTPException(status_code=404, detail="Failed to update records")


@app.delete("/delete/{id}")
async def delete_data(id: int):
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("delete from data where id = ?", id)
        conn.commit()
        return {
            "code": 200,
            "message": "success",
            "details": "data deleted successfully"
        }

    except pyodbc.Error as e:
        print(f"Error while deleting records...{e}")
        raise HTTPException(status_code=404, detail="Failed to delete records")
