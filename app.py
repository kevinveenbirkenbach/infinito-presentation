import os
import subprocess
from flask import Flask
from flask import render_template
import glob
from jinja2 import Environment, FileSystemLoader
from utils.slide_extractor import extract_slide
from utils.list_snippets import list_snippets
from utils.background_helper import get_background
from utils.role_helper import list_roles_with_meta

app = Flask(__name__)

@app.template_global()
def roles(prefix=None, required_tags=None):
    return list_roles_with_meta("/source/roles", prefix=prefix, required_tags=required_tags)

# Register the SlideExtractor function in the Flask Jinja2 environment
@app.before_request
def register_extractor():
    app.jinja_env.globals['extract_slide'] = extract_slide
    
@app.template_global()
def snippets(subdir):
    return list_snippets(app.template_folder, subdir)

# Register the function globally for Jinja2
@app.template_global()
def background(file_path):
    return get_background(app.template_folder, file_path)

@app.route('/')
def index():
    return render_template('presentation.html.j2')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
