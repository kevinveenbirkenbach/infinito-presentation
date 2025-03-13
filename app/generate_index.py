import os
import glob
import markdown
from jinja2 import Template

# Base directory containing the README files
BASE_DIR = "../cymais/roles"

# Reveal.js HTML template
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyMaIS Presentation</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reveal.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/theme/black.min.css">
</head>
<body>
    <div class="reveal">
        <div class="slides">
            {% for title, content in slides %}
            <section>
                <h2>{{ title }}</h2>
                <div>{{ content | safe }}</div>
            </section>
            {% endfor %}
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.3.1/reveal.min.js"></script>
    <script> Reveal.initialize(); </script>
</body>
</html>
"""

def find_readmes():
    """Find all README files in a case-insensitive way."""
    all_files = glob.glob(os.path.join(BASE_DIR, "**/*"), recursive=True)  # Get all files
    readmes = [f for f in all_files if os.path.basename(f).lower() == "readme.md"]

    # Include other documentation files from the base directory
    doc_files = glob.glob(f"{BASE_DIR}/*.md")
    
    return readmes + doc_files

print(find_readmes())

def generate_html():
    """Generate the presentation HTML from README files."""
    readmes = find_readmes()
    slides = []

    for readme in readmes:
        with open(readme, "r", encoding="utf-8") as f:
            md_content = f.read()
            md_content = md_content.replace("{{", "{% raw %}{{").replace("}}", "}}{% endraw %}")
            html_content = markdown.markdown(md_content)

            title = os.path.basename(os.path.dirname(readme)).replace("-", " ").title()
            slides.append((title, html_content))

    # Render HTML using Jinja2
    template = Template(TEMPLATE)
    html_output = template.render(slides=slides)

    # Save as index.html.j2
    output_path = os.path.join("templates", "index.html.j2")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_output)
    
    print(f"index.html.j2 successfully generated at {output_path}")

if __name__ == "__main__":
    generate_html()
