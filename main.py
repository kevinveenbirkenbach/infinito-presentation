import os
import glob
import markdown
from jinja2 import Environment, FileSystemLoader

# Base directory containing the README files
BASE_DIR = "../source"

def find_readmes():
    """Find all README files in a case-insensitive way."""
    all_files = glob.glob(os.path.join(BASE_DIR, "**/*"), recursive=True)  # Get all files
    readmes = [f for f in all_files if os.path.basename(f).lower() == "readme.md"]

    # Include other documentation files from the base directory
    doc_files = glob.glob(f"{BASE_DIR}/*.md")
    
    return readmes + doc_files

def generate_html():
    """Generate the presentation HTML from README files using a Jinja2 template file."""
    readmes = find_readmes()
    slides = []

    for readme in readmes:
        with open(readme, "r", encoding="utf-8") as f:
            md_content = f.read()
            md_content = md_content.replace("{{", "{% raw %}{{").replace("}}", "}}{% endraw %}")
            html_content = markdown.markdown(md_content)

            title = os.path.basename(os.path.dirname(readme)).replace("-", " ").title()
            slides.append((title, html_content))

    # Set up Jinja2 environment and load the template file
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("presentation.html.j2")

    # Render HTML using the template
    html_output = template.render(slides=slides)

    # Save as index.html.j2
    output_path = os.path.join("static", "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_output)
    
    print(f"index.html successfully generated at {output_path}")

if __name__ == "__main__":
    generate_html()
