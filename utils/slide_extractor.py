import re
import os
import markdown
from jinja2 import Environment, FileSystemLoader

class SlideExtractor:
    def __init__(self, file_path, headline=None):
        self.file_path = file_path
        self.headline = headline
        self.md_content = self._read_file()

    def _read_file(self):
        """Reads the content of the given file based on its type (MD, J2, or HTML)."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _convert_to_html(self, content):
        """Converts markdown content to HTML."""
        return markdown.markdown(content)

    def _process_jinja2(self, content):
        """Processes Jinja2 content and renders it with the environment."""
        # Initialize Jinja2 environment
        env = Environment(loader=FileSystemLoader(os.path.dirname(self.file_path)))
        template = env.from_string(content)
        return template.render()

    def _get_headline_content(self, content):
        """Extracts content under a specific headline in markdown format."""
        if self.headline:
            # Regular expression to search for the specific headline in markdown
            pattern = re.compile(r"^(#{1,6})\s+" + re.escape(self.headline.strip()) + r"\s*$", re.MULTILINE)
            match = pattern.search(content)

            if match:
                # Find the level of the headline (number of '#' characters)
                headline_level = len(match.group(1))
                title = self.headline.strip()

                # Start extracting content after the found headline
                content_start_index = match.end()

                # Search for the next headline of the same or higher level
                next_header_pattern = re.compile(r"^(#{1," + str(headline_level) + r"})\s+.*$", re.MULTILINE)
                next_header_match = next_header_pattern.search(content[content_start_index:])

                if next_header_match:
                    # Extract content until the next matching or higher-level headline
                    content_end_index = content_start_index + next_header_match.start()
                    section_content = content[content_start_index:content_end_index].strip()
                else:
                    # If no next matching header is found, extract all remaining content
                    section_content = content[content_start_index:].strip()

                # Convert the extracted markdown content to HTML
                return title, self._convert_to_html(section_content)
            else:
                return "Headline not found", ""
        else:
            return os.path.basename(os.path.dirname(self.file_path)).replace("-", " ").title(), self._convert_to_html(content)

    def get_content(self):
        """Main method to get content based on the file type (MD, J2, or HTML)."""
        _, file_extension = os.path.splitext(self.file_path)

        if file_extension == ".md":
            # If the file is Markdown, extract content under the specified headline
            title, content = self._get_headline_content(self.md_content)
        elif file_extension == ".j2":
            # If the file is Jinja2, render it as a template
            title = "Jinja2 Template"
            content = self._process_jinja2(self.md_content)
        elif file_extension == ".html":
            # If the file is HTML, just return the content
            title = "HTML Content"
            content = self.md_content
        else:
            title = "Unsupported file type"
            content = ""

        return {
            "title": title,
            "content": content
        }

# Function to register SlideExtractor as a Jinja2 function
def extract_slide(file_path, headline=None):
    slide_extractor = SlideExtractor(file_path, headline)
    return slide_extractor.get_content()