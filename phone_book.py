import sqlite3
import json

# conncecting to DB
conn = sqlite3.connect("connects.db")
cur = conn.cursor()

# Data example
example = {
    "contacts": [
        {
            "name": "myName",
            "mobile": "00-000000000",
            "home": "48/c",
            "email": "xxx@gmail.com"
        }
    ]
}


# create table for database with columns name , mobile, home address, email
# cur.execute("""CREATE TABLE contacts ("id" INTEGER NOT NULL,
# "name" TEXT,
# "home" TEXT,
# "email" TEXT,
# PRIMARY KEY ("id" AUTOINCREMENT))""")

def create(data):
    for contact in data["contacts"]:
        try:
            cur.execute(f'INSERT INTO contacts (name, mobile, home, email) VALUES'
                        f'("{contact["name"]}"), "{contact["mobile"]}", "{contact["home"]}","{contact["email"]}")')
        except sqlite3.OperationalError as err:
            print(err)
            return
        conn.commit()
        print("New Record Added")
        return


def read(name=None):
    if not name:
        name = ""

    cur.execute(f'SELECT * FROM contacts WHERE "name" LIKE "%{name}%"')
    rows = cur.fetchall()
    records = {"results": []}

    for row in rows:
        record = {"name": row[1], "mobile": row[2], "home": row[3], "email": row[4]}
        records["results"].append(record)

    pretty_records = json.dumps(records, indent=2)

    print(pretty_records)
    return


read()
