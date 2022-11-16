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
@app.route('/pets', methods=["GET", "POST"])
def pets():
    if request.method == "GET":
        query = "SELECT Pets.pet_id AS PetID, Shelters.name AS Shelter, Fosters.name AS Foster, type AS Type, weight AS Weight, is_kid_friendly AS KidFriendly, Pets.name AS Name, age AS Age, breed AS Breed, gender AS Gender, is_adopted AS Adopted FROM Pets JOIN Shelters ON Pets.shelter_id = Shelters.shelter_id LEFT JOIN Fosters ON Pets.foster_id = Fosters.foster_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT Shelters.shelter_id, Shelters.name AS Shelter from Shelters ORDER BY Shelters.name ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        shelter_data = cur.fetchall()

        query3 = "SELECT Fosters.foster_id, Fosters.name AS Foster FROM Fosters"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        foster_data = cur.fetchall()

        return render_template("pets.j2", data=data, shelter_data=shelter_data, foster_data=foster_data)
    
    if request.method == "POST":
        if request.form.get("Add_Pet"):
            shelter_id = request.form["shelter"]
            foster_id = request.form["foster"]
            type = request.form["type"]
            weight = request.form["weight"]
            is_kid_friendly = request.form["is_kid_friendly"]
            name = request.form["name"]
            age = request.form["age"]
            breed = request.form["breed"]
            gender = request.form["gender"]
            is_adopted = request.form["is_adopted"]
            
            query = "INSERT INTO Pets (shelter_id, foster_id, type, weight, is_kid_friendly, name, age, breed, gender, is_adopted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (shelter_id, foster_id, type, weight, is_kid_friendly, name, age, breed, gender, is_adopted))
            mysql.connection.commit()
        
        return redirect("/pets")


# Adopters page routes
@app.route('/adopters', methods=["POST", "GET"])
def adopters():
    if request.method == "POST":
        if request.form.get("Add_Adopter"):
            first_name = request.form["adopter_fname"]
            last_name = request.form["adopter_lname"]
            phone_number = request.form["adopter_phone"]
            email = request.form["adopter_email"]
            city = request.form["adopter_city"]
            state = request.form["adopter_state"]
            number_of_pets = request.form["number_of_pets"]
            has_kid = request.form["has_kid"]
            looking_for = request.form["looking_for"]

            query = "INSERT INTO Adopters (first_name, last_name, phone_number, email, city, state, number_of_pets, has_kid, looking_for) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, phone_number, email, city, state, number_of_pets, has_kid, looking_for))
            mysql.connection.commit()
        
        return redirect("/adopters")

    if request.method == "GET":
        query = "SELECT * FROM Adopters"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("adopters.j2", data=data)

# edit an adopter
@app.route("/edit_adopter/<int:adopter_id>", methods=["POST", "GET"])
def edit_adopter(adopter_id):
    if request.method == "GET":
        query = "SELECT * FROM Adopters WHERE adopter_id = %s" % (adopter_id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_adopter.j2", data=data)
    
    if request.method == "POST":
        if request.form.get("Edit_Adopter"):
            first_name = request.form["adopter_fname"]
            last_name = request.form["adopter_lname"]
            phone_number = request.form["adopter_phone"]
            email = request.form["adopter_email"]
            city = request.form["adopter_city"]
            state = request.form["adopter_state"]
            number_of_pets = request.form["number_of_pets"]
            has_kid = request.form["has_kid"]
            looking_for = request.form["looking_for"]
        
        query = "UPDATE Adopters SET Adopters.first_name = %s, Adopters.last_name = %s,Adopters.phone_number = %s, Adopters.email = %s, Adopters.city = %s, Adopters.state = %s, Adopters.number_of_pets = %s, Adopters.has_kid = %s, Adopters.looking_for = %s WHERE Adopters.adopter_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (first_name, last_name, phone_number, email, city, state, number_of_pets, has_kid, looking_for, adopter_id))
        mysql.connection.commit()

        return redirect("/adopters")

# delete an adopter
@app.route("/delete_adopter/<int:adopter_id>")
def delete_adopter(adopter_id):

    query = "DELETE FROM Adopters WHERE adopter_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (adopter_id,))
    mysql.connection.commit()

    return redirect("/adopters")

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

# edit a foster
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

#delete a foster
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

# edit a shelter
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

# delete a shelter
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

        query2 = "SELECT Shelters.shelter_id, CONCAT(Shelters.name, ',ID: ', Shelters.shelter_id) AS Shelter FROM Shelters ORDER BY Shelters.name ASC;"
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
