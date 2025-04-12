import os
from utils.base_config_loader import BaseConfigLoader


class DocsLinkService(BaseConfigLoader):
    """
    Service class for generating documentation links based on configuration.

    Usage:
        service = DocsLinkService("config.yml")
        link = service.generate_link("/source/docs/overview/Problem_Statement.md")
    """

    def __init__(self, config_path: str):
        super().__init__(config_path)

    def generate_link(self, source_path: str) -> str:
        """
        Generate a documentation link from a source file path.

        Converts .md to .html and removes the '/source/' prefix.

        Args:
            source_path (str): The source file path (e.g., '/source/docs/overview/Problem_Statement.md').

        Returns:
            str: The generated documentation link.
        """
        base_url = self.get("docs_base_url", "/docs/")
        if not base_url.endswith("/"):
            base_url += "/"

        if source_path.endswith(".md"):
            source_path = source_path[:-3] + ".html"

        if source_path.startswith("/source/"):
            source_path = source_path[len("/source/"):]

        return base_url + source_path
