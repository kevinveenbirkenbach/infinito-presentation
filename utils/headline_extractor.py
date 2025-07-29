import re

def slugify(value):
    return value.lower().replace(" ", "-")

def extract_first_headline(file_path):
    import re
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for beaver_section usage
    beaver_match = re.search(r"{{\s*beaver_section\(\s*['\"](.*?)['\"]", content)
    if beaver_match:
        headline = beaver_match.group(1).strip()
        return slugify(headline), headline

    # Fallback: existing logic
    section_match = re.search(r"<section([^>]*)>(.*?)</section>", content, re.DOTALL)
    section_id = None
    section_content = ""

    if section_match:
        section_attrs = section_match.group(1)
        section_content = section_match.group(2)
        id_match = re.search(r'id="([^"]+)"', section_attrs)
        section_id = id_match.group(1) if id_match else None

    set_match = re.search(r"{%\s*set\s+headline\s*=\s*['\"](.*?)['\"]\s*%}", content)
    if set_match:
        headline = set_match.group(1).strip()
        section_id = slugify(headline)
        return section_id, headline

    h_match = re.search(r"<h[1-6][^>]*>(.*?)</h[1-6]>", section_content, re.DOTALL)
    if h_match:
        return section_id, h_match.group(1).strip()

    return section_id, None


