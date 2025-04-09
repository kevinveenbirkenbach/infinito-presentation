import os
import subprocess
from flask import Flask
from flask import render_template
import glob
from jinja2 import Environment, FileSystemLoader
from utils.slide_extractor import extract_slide

app = Flask(__name__)

# Register the SlideExtractor function in the Flask Jinja2 environment
@app.before_request
def register_slide_extractor():
    app.jinja_env.globals['extract_slide'] = extract_slide

@app.route('/')
def index():
    return render_template('presentation.html.j2')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
