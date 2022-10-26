import os
from flask import Flask, render_template

# Configuration

app = Flask(__name__)

# Routes


@app.route('/')
def root():
    return render_template("main.j2")

# Listener


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)
