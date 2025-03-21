import os
import glob
import markdown
import argparse
from jinja2 import Environment, FileSystemLoader

def find_readmes(source_dir):
    """Find all README files in a case-insensitive way."""
    all_files = glob.glob(os.path.join(source_dir, "**/*"), recursive=True)  # Get all files
    readmes = [f for f in all_files if os.path.basename(f).lower() == "readme.md"]

    # Include other documentation files from the base directory
    doc_files = glob.glob(f"{source_dir}/*.md")
    
    return readmes + doc_files

def generate_html(source_dir, output_dir_path):
    """Generate the presentation HTML from README files using a Jinja2 template file."""
    readmes = find_readmes(source_dir)
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

    # Save the rendered HTML to the output file
    with open(f"{output_dir_path}/index.html", "w", encoding="utf-8") as f:
        f.write(html_output)
    
    print(f"HTML successfully generated at {output_dir_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate presentation HTML from README markdown files."
    )
    # Hier werden positionsbasierte Argumente definiert, die obligatorisch sind.
    parser.add_argument("source", help="Path to the source directory containing README files.")
    parser.add_argument("output", help="Path to the output HTML file.")

    args = parser.parse_args()
    generate_html(args.source, args.output)
