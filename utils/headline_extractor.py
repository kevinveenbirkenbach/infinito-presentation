# utils/headline_extractor.py
import re

def slugify(value):
    return value.lower().replace(" ", "-")

def extract_first_headline(file_path):
    """
    Extracts the first headline from a template.

    Priority:
    - First `{% set headline = '...' %}` anywhere in the file -> id = slugify(headline)
    - Otherwise first <h1> to <h6> inside the first <section> (with id if available)
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find first <section>
    section_match = re.search(r"<section([^>]*)>(.*?)</section>", content, re.DOTALL)
    section_id = None
    section_content = ""

    if section_match:
        section_attrs = section_match.group(1)
        section_content = section_match.group(2)
        id_match = re.search(r'id="([^"]+)"', section_attrs)
        section_id = id_match.group(1) if id_match else None

    # Check for headline set in full content
    set_match = re.search(r"{%\s*set\s+headline\s*=\s*['\"](.*?)['\"]\s*%}", content)

    if set_match:
        headline = set_match.group(1).strip()
        section_id = slugify(headline)
        return section_id, headline

    # Otherwise search for first h1-h6 in first section
    h_match = re.search(r"<h[1-6][^>]*>(.*?)</h[1-6]>", section_content, re.DOTALL)

    if h_match:
        return section_id, h_match.group(1).strip()

    return section_id, None
