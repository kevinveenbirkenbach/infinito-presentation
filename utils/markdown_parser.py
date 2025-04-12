import re

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
    def extract_section(content: str, section_name: str) -> str:
        """
        Extracts the content of a specific markdown section.

        Args:
            content (str): The markdown content.
            section_name (str): The name of the section to extract.

        Returns:
            str: The extracted section content.
        """
        pattern = rf"(?:##\s+(?:\d+\.\s+)?{re.escape(section_name)})(.*?)(?:\n##|\Z)"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

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
