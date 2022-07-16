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
#"mobile" TEXT,
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


def _update_number(row):
    mobile = input("Enter a new mobile number (skip to leave unchanged): ")
    home = input("Enter a new home address (skip to leave unchanged): ")
    email = input("Enter a new email (skip to leave unchanged): ")

    mobile = mobile if mobile != "" else row[2]
    home = home if home != "" else row[3]
    email = email if email != "" else row[4]

    cur.execute(f'UPDATE contacts SET mobile="{mobile}", home="{home}", email="{email}"'
                f'WHERE name="{row[1]}"')

    conn.commit()
    return


def update(name):
    cur.execute(f'SELECT * FROM contacts WHERE "name" LIKE "%{name}%"')
    rows = cur.fetchall()

    if len(rows) == 1:
        row = rows[0]
        _update_number(row)
    else:
        print("Multiple results were found. Select which one:")
        for row in rows:
            print(row)

        _id = input("Enter number here: ")
        cur.execute(f'SELECT * FROM contacts WHERE id={_id}')
        row = cur.fetchall()[0]
        _update_number(row)

    print("Number Updated")


def _delete_number(row):
    cur.execute(f'DELETE FROM contacts WHERE id={row[0]}')
    conn.commit()
    return


def delete(name):
    cur.execute(f'SELECT * FROM contacts WHERE "name" LIKE "%{name}%"')
    rows = cur.fetchall()

    if len(rows) == 1:
        row = rows[0]
        _delete_number(row)
    else:
        print("Multiple results were found. Select which one:")
        for row in rows:
            print(row)

        _id = input("Enter number here: ")
        cur.execute(f'SELECT * FROM contacts WHERE id={_id}')
        row = cur.fetchall()[0]
        _delete_number(row)

    print("Number Deleted")


# Main logic
def main():
    while True:
        options = input("SELECT one of the options: Create (C) Real (R) Update (U) delete (D) or quit (Q)")

        if options.lower() == "c":
            new_record = {
                "contacts": [
                    {
                        "name": input("Enter a name: "),
                        "mobile": input("Enter a number: "),
                        "home": input("Enter an address: "),
                        "email": input("Enter email: ")
                    }
                ]
            }

            create(new_record)
        elif options.lower() == "r":
            name = input("Enter a name: ")
            read(name)
        elif options.lower() == "u":
            name = input("Enter a name: ")
            update(name)
        elif options.lower() == "d":
            name = input("Enter a name: ")
            delete(name)
        elif options.lower() == "q":
            print("Bye Bye")
            quit()
        else:
            print(f"No option {options} available")


if __name__ == "__main__":
    main()