# utils/headline_extractor.py
import os
import re
from jinja2 import Environment, FileSystemLoader

def extract_first_headline(file_path):
    """
    Extracts the first headline (h1-h6) from the first <section> in a template.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Suche nach der ersten Section
    section_match = re.search(r"<section([^>]*)>(.*?)</section>", content, re.DOTALL)
    if not section_match:
        return None, None

    section_attrs = section_match.group(1)
    section_content = section_match.group(2)

    # Suche nach ID
    id_match = re.search(r'id="([^"]+)"', section_attrs)
    section_id = id_match.group(1) if id_match else None

    # Suche nach erster Headline
    headline_match = re.search(r"<h[1-6][^>]*>(.*?)</h[1-6]>", section_content, re.DOTALL)
    headline = headline_match.group(1).strip() if headline_match else None

    return section_id, headline
