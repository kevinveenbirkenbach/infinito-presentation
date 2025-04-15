import re
import markdown

class MarkdownParser:
    """Utility class for extracting information from Markdown content."""

    @staticmethod
    def extract_title(content: str) -> str:
        """
        Extracts the first Markdown headline from the content.
        
        Args:
            content (str): The markdown content.
        
        Returns:
            str: The extracted title or 'Unknown'.
        """
        match = re.search(r"^#\s+(.*)$", content, re.MULTILINE)
        return match.group(1).strip() if match else "Unknown"


    @staticmethod
    def extract_section(content: str, section_name: str, output_type: str = "html"):
        pattern = rf"(?:^|\n)#+\s*{re.escape(section_name)}\s*\n(.*?)(?=\n#+\s|\Z)"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if not match:
            return "" if output_type == "html" else []

        section_content = match.group(1).strip()

        if output_type == "list":
            items = re.findall(r"^\s*[-*+]\s+(.*)", section_content, re.MULTILINE)
            return [markdown.markdown(item.strip()) for item in items]

        return markdown.markdown(section_content)

    @staticmethod
    def extract_mermaid_diagrams(content: str) -> list:
        """
        Extracts Mermaid diagrams from markdown content.

        Args:
            content (str): The markdown content.

        Returns:
            list: A list of mermaid diagram code blocks.
        """
        return re.findall(r"```mermaid(.*?)```", content, re.DOTALL)
