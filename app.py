import os
from flask import Flask, render_template

# Configuration

app = Flask(__name__)

# Routes


@app.route('/')
def root():
    return render_template("home.html")


@app.route('/pets')
def pets():
    return render_template("pets.j2")


@app.route('/adopters')
def adopters():
    return render_template("adopters.j2")


@app.route('/fosters')
def fosters():
    return render_template("fosters.j2")


@app.route('/shelters')
def shelters():
    return render_template("shelters.j2")


@app.route('/foster_shelters')
def foster_shelters():
    return render_template("foster_shelters.j2")


@app.route('/adoption_records')
def adoption_records():
    return render_template("adoption_records.j2")
# Listener


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)
