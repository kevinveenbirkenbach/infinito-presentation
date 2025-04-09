import os
import subprocess
from flask import Flask
from flask import render_template
import os
import glob
import markdown
import argparse

def find_readmes(source_dir):
    """Find all README files in a case-insensitive way."""
    all_files = glob.glob(os.path.join(source_dir, "**/*"), recursive=True)  # Get all files
    readmes = [f for f in all_files if os.path.basename(f).lower() == "readme.md"]

    # Include other documentation files from the base directory
    doc_files = glob.glob(f"{source_dir}/*.md")
    
    return readmes + doc_files

def get_slide(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        md_content = f.read()
        md_content = md_content.replace("{{", "{% raw %}{{").replace("}}", "}}{% endraw %}")
        html_content = markdown.markdown(md_content)
        title = os.path.basename(os.path.dirname(file_path)).replace("-", " ").title()
    return {
        "title": title,
        "content": html_content
        }

def get_slide_data(source_dir="/source"):
    """Generate the presentation HTML from README files using a Jinja2 template file."""
    readmes = find_readmes(source_dir)
    slides = []

    for readme in readmes:
        slides.append(get_slide(readme))
    return slides

def get_slides_composition():
    pass

app = Flask(__name__)

@app.route('/')
def index():
    slides_data = get_slide_data()
    return render_template('presentation.html.j2', slides=slides_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
