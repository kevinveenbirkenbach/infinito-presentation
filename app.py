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
from utils.docs_link_generator import generate_docs_link
from utils.app_url_generator import generate_app_url 
from utils.headline_extractor import extract_first_headline

app = Flask(__name__)

@app.template_global()
def headlines(subdir):
    files = list_snippets(app.template_folder, subdir)
    result = []

    for file in files:
        file_path = os.path.join(app.template_folder, file)
        section_id, headline = extract_first_headline(file_path)

        if headline:
            result.append({
                "id": section_id,
                "headline": headline
            })

    return result

@app.template_global()
def app_url(application_id):
    """Generate an application URL based on the given application ID."""
    return generate_app_url(application_id)

@app.template_global()
def docs_link(source_path):
    """Return a documentation link based on the given source path."""
    return generate_docs_link(source_path)

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
