import os
import sqlite3
import csv
import json

# Define file paths
DATABASE = "example.db"
CSV_FILE_1 = "data/presidents-1.csv"
CSV_FILE_2 = "data/presidents-2.csv"
JSON_FILE_1 = "data/presidents-3.json"
JSON_FILE_2 = "data/presidents-4.json"


def query_db(cur, query, args=(), one=False):
    cur = cur.execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


# If database (in case of SQLite this is a text file) doesn't exist
if not os.path.exists(DATABASE):
    # Create text file
    with open(DATABASE, "w"):
        pass
# If database exists
else:
    # Delete database
    os.remove(DATABASE)

try:
    # Connect to database
    con = sqlite3.connect(DATABASE)
    print("Database successfully opened")
    # Provide both index-based and case-insensitive name-based access to columns
    con.row_factory = sqlite3.Row
    # Create cursor object
    cur = con.cursor()

    # Create table
    cur.execute(
        """CREATE TABLE president
        (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT
        )"""
    )

    # Insert row of data
    cur.execute("INSERT INTO president VALUES (1, 'George', 'Washington')")

    # Insert row of data without id
    cur.execute("INSERT INTO president (first_name, last_name) VALUES ('John', 'Adams')")

    # Insert data from csv file (qmark style)
    with open(CSV_FILE_1) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            cur.execute(
                "INSERT INTO president (first_name, last_name) VALUES (?, ?)", (row["first_name"], row["last_name"])
            )

    # Insert data from csv file (qmark style used with executemany())
    with open(CSV_FILE_2) as csv_file:
        csv_reader = csv.reader(csv_file)
        # Get all rows of csv from csv_reader object as list of tuples
        rows = [map(tuple, csv_reader)]
        cur.executemany(
            "INSERT INTO president (first_name, last_name) VALUES (?, ?)", rows[1:]
        )  # The [1:] prevents the header row (first row) from being inserted

    # Insert data from json file (qmark style)
    with open(JSON_FILE_1) as json_file:
        data = json.load(json_file)
        for row in data:
            cur.execute(
                "INSERT INTO president (first_name, last_name) VALUES (?, ?)", (row["first_name"], row["last_name"])
            )

    # Insert data from json file (qmark style used with executemany())
    with open(JSON_FILE_1) as json_file:
        data = json.load(json_file)
        rows = [tuple(row.values()) for row in data]
        cur.executemany("INSERT INTO president (first_name, last_name) VALUES (?, ?)", rows)

    # Retrieve all matching rows
    response = query_db(cur, "SELECT * FROM president WHERE first_name = 'James'")
    # Print whole row
    print("EXAMPLE 1.1")
    for row in response:
        print(*row)
    # Print parts of row index-based
    print("EXAMPLE 1.2")
    for row in response:
        print(row[1], row[2])
    # Print parts of row case-insensite name-based
    print("EXAMPLE 1.3")
    for row in response:
        print(row["first_name"], row["LAST_NAME"])

    # Retrieve a single matching row
    response = query_db(cur, "SELECT * FROM president WHERE first_name = 'James'", one=True)
    # Print whole row
    print("EXAMPLE 2.1")
    print(*response)
    # Print parts of row index-based
    print("EXAMPLE 2.2")
    print(response[1], response[2])    
     # Print parts of row case-insensite name-based
    print("EXAMPLE 2.3")
    print(response["first_name"], response["LAST_NAME"])       

    # Retrieve a single matching row with placerholder
    name = "James"
    response = query_db(cur, "SELECT * FROM president WHERE first_name = ?", (name, ) , True)
    print("EXAMPLE 3")
    print(*response)

    # Save changes
    con.commit()
    print("Changes saved")

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

finally:
    if con:
        con.close()
        print("Database connection closed")
