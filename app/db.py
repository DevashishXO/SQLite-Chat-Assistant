import sqlite3

DB_PATH = "data/database.sqlite"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Employees(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT NOT NULL,
                    Department TEXT NOT NULL,
                    Salary INTEGER NOT NULL,
                    Hire_Date TEXT NOT NULL
                    )
    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Departments(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Manager TEXT NOT NULL  
                ) 
    ''')

    employees = [
        (1, 'Alice', 'Sales', 50000, '2021-01-15'),
        (2, 'Bob', 'Engineering', 70000, '2020-06-10'),
        (3, 'Charlie', 'Marketing', 60000, '2022-03-20')
    ]

    departments = [
        (1, 'Sales', 'Alice'),
        (2, 'Engineering', 'Bob'),
        (3, 'Marketing', 'Charlie')
    ]

    cursor.executemany('INSERT INTO Employees VALUES (?,?,?,?,?)', employees)
    cursor.executemany('INSERT INTO Departments VALUES (?,?,?)', departments)

    conn.commit()
    conn.close()



if __name__ == "__main__":
    create_tables()



