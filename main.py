import pyodbc
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


class User(BaseModel):
    person_id: int
    name: str
    email: str
    password: str
    city: str


def create_conn():
    try:
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server=Enter server details'
                              'Database=database name;'
                              'Trusted_Connection=yes;')
        cursor = conn.cursor()
        if cursor:
            print("connection successfully")
        else:
            print("No curser available...")
        return conn

    except pyodbc.Error as e:
        print(f"connection Failed..{e}")
        raise HTTPException(status_code=500, detail="Database connection error...")


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
            sets.append(row)
        sets.append(list(set_))

        if cursor.nextset() is None or cursor.description is None:
            break
    return sets


@app.get('/record')
async def get_data():
    try:
        cur = create_conn().cursor()
        cur.execute("select * from abc")
        data = resultset(cur)
        return {
            "code": 200,
            "data": data
        }

    except pyodbc.Error as e:
        print(f"Error while fetching data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve records")


@app.get('/record_id{person_id}')
async def get_id_data(person_id: int):
    try:
        connection = create_conn()
        cur = connection.cursor()
        cur.execute("select * from abc where PersonID = ?", person_id)
        data_id = resultset(cur)
        return {
            "code": 200,
            "data": data_id
        }

    except pyodbc.Error as e:
        print(f"Error while fetching data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve records")


@app.post('/add_user/')
async def create_user(user: User):
    try:
        connection = create_conn()
        cur = connection.cursor()
        cur.execute("insert into abc (PersonID, Name, Email, Password, City) values (?,?,?,?,?)",
                    (user.person_id, user.name, user.email, user.password, user.city))
        connection.commit()
        return {
            "code": 200,
            "data": "user created succefully..."
        }

    except pyodbc.Error as e:
        print(f"Error while fetching data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve records")


@app.put('/update/{person_id}')
async def update_data(person_id: int, user: User):
    try:
        connection = create_conn()
        cur = connection.cursor()

        cur.execute(
            "UPDATE abc SET Name = ?, Email = ?, Password = ?, City = ? WHERE PersonID = ? ",
            (user.name, user.email, user.password, user.city, person_id)
        )

        connection.commit()
        return {
            "code": 200,
            "message": "data update successfully..."
        }
    except pyodbc.Error as e:
        print(f"Error while fetching data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve records")


@app.delete('/record_id{person_id}')
async def get_id_data(person_id: int):
    try:
        connection = create_conn()
        cur = connection.cursor()
        cur.execute("delete from abc where PersonID = ?", person_id)
        connection.commit()
        return {
            "code": 200,
            "data": "Data deleted successfully..."
        }

    except pyodbc.Error as e:
        print(f"Error while fetching data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve records")
