# utils/headline_extractor.py
import re

def slugify(value):
    return value.lower().replace(" ", "-")

def extract_first_headline(file_path):
    """
    Extracts the first headline from a template.

    Priority:
    - First `{% set headline = '...' %}` anywhere in the file.
    - OR first <h1> to <h6> inside the first <section> (whichever comes first).

    If headline is set via `{% set headline = '...' %}` -> id = headline | lower | replace(' ', '-')
    Otherwise extracts id from the first <section> (if available).
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
        # Extract id from section
        id_match = re.search(r'id="([^"]+)"', section_attrs)
        section_id = id_match.group(1) if id_match else None

    # Pattern to search for headline set or h1-h6 tag
    pattern = r"""
        (                              # Group 1: headline set
            {%\s*set\s+headline\s*=\s*['"](.*?)['"]\s*%}
        )
        |
        (                              # Group 3: h1-h6 tag
            <h[1-6][^>]*>(.*?)</h[1-6]>
        )
    """

    # Search for both in full content first
    set_match = re.search(pattern, content, re.DOTALL | re.VERBOSE)

    # Then search inside first <section> (if not already found)
    section_h_match = re.search(pattern, section_content, re.DOTALL | re.VERBOSE)

    # Decide which match comes first
    if set_match and (not section_h_match or set_match.start() < section_match.start() + section_h_match.start(0)):
        if set_match.group(2):
            headline = set_match.group(2).strip()
            section_id = slugify(headline)
            return section_id, headline
    elif section_h_match:
        if section_h_match.group(2):
            return section_id, section_h_match.group(2).strip()
        if section_h_match.group(4):
            return section_id, section_h_match.group(4).strip()

    return section_id, None
