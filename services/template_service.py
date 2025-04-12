import os
from utils.file_finder import FileFinder


class TemplateService:
    """
    Service class for managing template snippets.

    Usage:
        service = TemplateService(template_folder="templates")
        snippets = service.list_snippets("slides/features")
    """

    def __init__(self, template_folder: str):
        self.template_folder = template_folder

    def list_snippets(self, subdir: str, suffix: str = ".html.j2", relative_paths: bool = True) -> list:
        """
        List all snippet files in a given subdirectory.

        Args:
            subdir (str): Subdirectory path relative to the template folder.
            suffix (str, optional): Only include files ending with this suffix. Defaults to ".html.j2".
            relative_paths (bool, optional): If True, return relative paths. Defaults to True.

        Returns:
            list: Sorted list of matching snippet paths.

        Raises:
            ValueError: If no files were found.
        """
        dir_path = os.path.join(self.template_folder, subdir)

        files = FileFinder.find_files(dir_path, suffix)

        if not files:
            raise ValueError(f"No files with suffix '{suffix}' found in '{dir_path}'")

        if relative_paths:
            return [os.path.join(subdir, file) for file in files]
        return files
