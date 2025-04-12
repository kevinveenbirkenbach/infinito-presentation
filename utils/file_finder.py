import os


class FileFinder:
    """Utility class for file system operations."""

    @staticmethod
    def find_files(directory: str, suffix: str = "") -> list:
        """
        Finds all files in a directory with a given suffix.

        Args:
            directory (str): The directory path to search.
            suffix (str, optional): The file suffix to filter by (e.g., ".html.j2"). Defaults to "".

        Returns:
            list: Sorted list of matching filenames.
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}")

        return sorted(
            f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f)) and f.endswith(suffix)
        )
