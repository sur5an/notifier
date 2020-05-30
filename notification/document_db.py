import sqlite3 as lite


def create_schema():
    con = lite.connect('document.db')

    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS documents")
        cur.execute("CREATE TABLE documents(Id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "DocumentName TEXT, DateOfExpire TEXT, UserName TEXT, "
                    "DocumentDescription TEXT, RemindStart TEXT, RemindFrequency TEXT)")


def insert_all(records):
    con = lite.connect('document.db')
    with con:
        cur = con.cursor()
        for record in records:
            sql = "INSERT INTO documents (DocumentName, DateOfExpire, UserName, " \
                        "DocumentDescription, RemindStart, RemindFrequency) VALUES("
            sql += "\"" + "\", \"".join(record) + "\")"
            cur.execute(sql)


if __name__ == '__main__':
    create_schema()
