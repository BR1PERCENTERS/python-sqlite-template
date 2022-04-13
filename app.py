import os
import sqlite3

DATABASE = "example.db"

# If database (in case of SQLite this is a text file) doesn't exist
if not os.path.exists(DATABASE):
    # Create text file
    with open(DATABASE, "w"):
        pass

try:
    # Connect to database
    con = sqlite3.connect(DATABASE)
    print("Database successfully opened")
    # Create cursor object
    cur = con.cursor()
    # Create table
    cur.execute(
        """CREATE TABLE stocks
                (date text, trans text, symbol text, qty real, price real)"""
    )
    # Insert a row of data
    cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    # Save changes
    con.commit()
    print("Changes saved")
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
finally:
    if con:
        con.close()
        print("Database connection closed")
