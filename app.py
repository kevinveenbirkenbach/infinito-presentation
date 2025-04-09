import os
import subprocess
from flask import Flask

app = Flask(__name__)

# Generate index.html.j2 before starting the server
subprocess.run(["python", "main.py", "/source", "static"], check=True)

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
