from chalice import Chalice
import sqlite3 as sl

app = Chalice(app_name='dbout')


@app.route('/GM')
def index():
    db = sl.connect("marketplace.db")
    sql = db.cursor()
    data = ""
    for value in sql.execute("SELECT * FROM Market"):
        data += str(value) + "\n"

    return data


@app.route('/GA')
def index():
    db = sl.connect("garage.db")
    sql = db.cursor()
    data = ""
    for value in sql.execute("SELECT * FROM Cars"):
        data += str(value) + "\n"
    return data
