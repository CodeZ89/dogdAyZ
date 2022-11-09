import os
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request

# Configuration

app = Flask(__name__)

# database connection
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_clarkeab"
app.config["MYSQL_PASSWORD"] = "5328"
app.config["MYSQL_DB"] = "cs340_clarkeab"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes


@app.route('/')
def root():
    return render_template("home.j2")


@app.route('/pets', methods=["GET"])
def pets():
    if request.method == "GET":
        query = "SELECT * FROM Pets"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("pets.j2", data=data)


@app.route('/adopters', methods=["GET"])
def adopters():
    if request.method == "GET":
        query = "SELECT * FROM Adopters"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("adopters.j2", data=data)


@app.route('/fosters', methods=["GET"])
def fosters():
    if request.method == "GET":
        query = "SELECT * FROM Fosters"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("fosters.j2", data=data)


@app.route('/shelters', methods=["GET"])
def shelters():
    if request.method == "GET":
        query = "SELECT * FROM Shelters"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("shelters.j2", data=data)


@app.route('/foster_shelters', methods=["GET"])
def foster_shelters():
    if request.method == "GET":
        query = "SELECT * FROM Foster_shelters"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("foster_shelters.j2", data=data)


@app.route('/adoption_records', methods=["GET"])
def adoption_records():
    if request.method == "GET":
        query = "SELECT * FROM Adoption_records"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("adoption_records.j2", data=data)
# Listener


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4346))
    app.run(port=port, debug=True)
