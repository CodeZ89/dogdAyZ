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
    port = int(os.environ.get('PORT', 6969))
    app.run(port=port, debug=True)
