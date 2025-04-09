import re
import os
import markdown

def get_slide(file_path, headline=None):
    # Open the markdown file and read its content
    with open(file_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # If a headline is provided, extract the corresponding content
    if headline:
        # Regular expression to search for the specific headline in the markdown
        pattern = re.compile(r"^(#{1,6})\s+" + re.escape(headline.strip()) + r"\s*$", re.MULTILINE)
        match = pattern.search(md_content)
        
        if match:
            # Find the level of the headline (number of '#' characters)
            headline_level = len(match.group(1))
            title = headline.strip()

            # Start extracting content after the found headline
            content_start_index = match.end()

            # Search for the next headline of the same or higher level
            next_header_pattern = re.compile(r"^(#{1," + str(headline_level) + r"})\s+.*$", re.MULTILINE)
            next_header_match = next_header_pattern.search(md_content[content_start_index:])

            if next_header_match:
                # Extract content until the next matching or higher-level headline
                content_end_index = content_start_index + next_header_match.start()
                section_content = md_content[content_start_index:content_end_index].strip()
            else:
                # If no next matching header is found, extract all remaining content
                section_content = md_content[content_start_index:].strip()

            # Convert the extracted markdown content to HTML
            html_content = markdown.markdown(section_content)
        else:
            # If the headline is not found, return a default message
            title = "Headline not found"
            html_content = ""
    else:
        # If no headline is provided, use the directory name as the title
        title = os.path.basename(os.path.dirname(file_path)).replace("-", " ").title()
        # Convert the entire markdown file content to HTML
        html_content = markdown.markdown(md_content)

    # Return the title and the HTML content
    return {
        "title": title,
        "content": html_content
    }