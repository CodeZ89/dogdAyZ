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

# Pets page routes
@app.route('/pets', methods=["GET"])
def pets():
    if request.method == "GET":
        query = "SELECT * FROM Pets"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("pets.j2", data=data)

# Adopters page routes
@app.route('/adopters', methods=["GET"])
def adopters():
    if request.method == "GET":
        query = "SELECT * FROM Adopters"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("adopters.j2", data=data)

# Fosters page routes

# Read and Create Routes
@app.route('/fosters', methods=["POST","GET"])
def fosters():
    if request.method == "POST":
        if request.form.get("Add_Foster"):
            city = request.form["foster_city"]
            state = request.form["foster_state"]
            phone_number = request.form["foster_phone"]
            name = request.form["foster_name"]

            query = "INSERT INTO Fosters (city, state, phone_number, name) VALUES (%s, %s, %s, %s)"

            cur = mysql.connection.cursor()
            cur.execute(query, (city, state, phone_number, name))
            mysql.connection.commit()
        
        return redirect("/fosters")

    if request.method == "GET":
        query = "SELECT * FROM Fosters"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("fosters.j2", data=data)

@app.route("/edit_foster/<int:foster_id>", methods=["POST", "GET"])
def edit_foster(foster_id):
    if request.method == "GET":
        query = "SELECT * FROM Fosters WHERE foster_id = %s" % (foster_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_foster.j2", data=data)
    
    if request.method == "POST":
        if request.form.get("Edit_Foster"):
            foster_id = request.form["foster_id"]
            city = request.form["foster_city"]
            state = request.form["foster_state"]
            phone_number = request.form["foster_phone"]
            name = request.form["foster_name"]

            query = "UPDATE Fosters SET Fosters.city = %s, Fosters.state = %s, Fosters.phone_number = %s, Fosters.name = %s WHERE Fosters.foster_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (city, state, phone_number, name, foster_id))
            mysql.connection.commit()

            return redirect("/fosters")

@app.route("/delete_foster/<int:foster_id>")
def delete_foster(foster_id):

    query = "DELETE FROM Fosters WHERE foster_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (foster_id,))
    mysql.connection.commit()

    return redirect("/fosters")

# Shelters page routes
@app.route('/shelters', methods=["POST", "GET"])
def shelters():
    if request.method == "POST":
        if request.form.get("Add_Shelter"):
            city = request.form["shelter_city"]
            state = request.form["shelter_state"]
            phone = request.form["shelter_phone"]
            name = request.form["shelter_name"]
            number_of_pets = request.form["shelter_number_pet"]
            number_of_pets_foster = request.form["shelter_number_foster"]

            query = "INSERT INTO Shelters (city, state, phone_number, name, number_of_pets, number_of_pets_foster) VALUES (%s, %s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (city, state, phone, name,
                        number_of_pets, number_of_pets_foster))
            mysql.connection.commit()

        return redirect("/shelters")

    if request.method == "GET":
        query = "SELECT * FROM Shelters"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("shelters.j2", data=data)


@app.route("/edit_shelter/<int:shelter_id>", methods=["POST", "GET"])
def edit_shelter(shelter_id):
    if request.method == "GET":
        query = "SELECT * FROM Shelters WHERE shelter_id = %s" % (shelter_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_shelter.j2", data=data)

    if request.method == "POST":
        if request.form.get("Edit_Shelter"):
            shelter_id = request.form["shelter_id"]
            city = request.form["shelter_city"]
            state = request.form["shelter_state"]
            phone_number = request.form["shelter_phone"]
            name = request.form["shelter_name"]
            number_of_pets = request.form["shelter_number_pet"]
            number_of_pets_foster = request.form["shelter_number_foster"]

            query = "UPDATE Shelters SET Shelters.city = %s, Shelters.state = %s, Shelters.phone_number = %s, Shelters.name = %s, Shelters.number_of_pets = %s, Shelters.number_of_pets_foster = %s WHERE Shelters.shelter_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (city, state, phone_number, name,
                        number_of_pets, number_of_pets_foster, shelter_id))
            mysql.connection.commit()

            return redirect("/shelters")


@app.route("/delete_shelter/<int:shelter_id>")
def delete_shelter(shelter_id):

    query = "DELETE FROM Shelters WHERE shelter_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (shelter_id,))
    mysql.connection.commit()

    return redirect("/shelters")

# Foster-shelters page routes
@app.route('/foster_shelters', methods=["POST", "GET"])
def foster_shelters():
    if request.method == "GET":
        query = "SELECT Shelters.name AS Shelter, Fosters.name AS Foster FROM Foster_shelters JOIN Shelters ON Foster_shelters.shelter_id = Shelters.shelter_id JOIN Fosters ON Foster_shelters.foster_id = Fosters.foster_id ORDER BY Shelters.name ASC"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT Shelters.shelter_id, CONCAT(Shelters.name, ', ID: ', Shelters.shelter_id) as Shelter FROM Shelters ORDER BY Shelters.name ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        shelter_data = cur.fetchall()

        query3 = "SELECT Fosters.foster_id, CONCAT(Fosters.name, ', ID: ', Fosters.foster_id ) as Foster FROM Fosters"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        foster_data = cur.fetchall()

        return render_template("foster_shelters.j2", data=data, shelter_data=shelter_data, foster_data=foster_data)
    
    if request.method == "POST":
        if request.form.get("Add_Foster_Shelter"):
            shelter_id = request.form["shelter"]
            foster_id = request.form["foster"]

            query = "INSERT INTO Foster_shelters (shelter_id, foster_id) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (shelter_id, foster_id))
            mysql.connection.commit()

        return redirect("/foster_shelters")
    

"""@app.route('/delete_foster_shelters/<int:(shelter_id, foster_id)>')
def delete_foster_shelter(shelter_id, foster_id):
    query = "DELETE FROM Foster_shelters WHERE shelter_id = '%s' AND foster_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (shelter_id, foster_id))
    mysql.connection.commit()

    return redirect("/foster_shelters")"""


# adoption records page routes
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
    port = int(os.environ.get('PORT', 6969))
    app.run(port=port, debug=True)
