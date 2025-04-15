import os
import re
import markdown
from jinja2 import Environment, FileSystemLoader


class SlideService:
    """
    Service class for extracting slide content from markdown, jinja2, or HTML files.

    Usage:
        service = SlideService()
        content = service.extract_content("slides/example.md", headline="Introduction")
    """

    def __init__(self):
        pass

    @staticmethod
    def _read_file(file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def _convert_markdown_to_html(content: str) -> str:
        return markdown.markdown(content)

    def _render_jinja2(self, content: str, file_path: str) -> str:
        from flask import current_app

        env = Environment(loader=FileSystemLoader("templates"))
        env.globals.update(current_app.jinja_env.globals)

        template = env.from_string(content)
        return template.render()


    def _extract_markdown_section(self, content: str, headline: str) -> tuple:
        pattern = re.compile(r"^(#{1,6})\s+" + re.escape(headline.strip()) + r"\s*$", re.MULTILINE)
        match = pattern.search(content)

        if not match:
            return "Headline not found", ""

        level = len(match.group(1))
        start = match.end()
        next_headline = re.compile(r"^(#{1," + str(level) + r"})\s+.*$", re.MULTILINE)
        next_match = next_headline.search(content[start:])

        end = start + next_match.start() if next_match else len(content)
        section_content = content[start:end].strip()

        return headline.strip(), self._convert_markdown_to_html(section_content)

    def extract_content(self, file_path: str, headline: str = None, output_type: str = "html") -> dict:
        content = self._read_file(file_path)
        _, ext = os.path.splitext(file_path)

        if ext == ".md":
            if headline:
                if output_type == "list":
                    from utils.markdown_parser import MarkdownParser
                    return {
                        "title": headline,
                        "content": MarkdownParser.extract_section(content, headline, output_type="list")
                    }
                else:
                    title, html_content = self._extract_markdown_section(content, headline)
            else:
                title = os.path.basename(os.path.dirname(file_path)).replace("-", " ").title()
                html_content = self._convert_markdown_to_html(content)

        elif ext == ".j2":
            title = "Jinja2 Template"
            html_content = self._render_jinja2(content, file_path)

        elif ext == ".html":
            title = "HTML Content"
            html_content = content

        else:
            title = "Unsupported file type"
            html_content = ""

        return {
            "title": title,
            "content": html_content
        }

