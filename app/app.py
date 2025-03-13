import os
import subprocess
from flask import Flask, render_template

app = Flask(__name__)

# Generate index.html.j2 before starting the server
subprocess.run(["python", "generate_index.py"], check=True)

@app.route('/')
def index():
    return render_template("index.html.j2")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
