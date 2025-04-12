import os
import yaml
from utils.file_finder import FileFinder


class RoleService:
    """
    Service class for listing roles and extracting metadata.

    Usage:
        service = RoleService("/source/roles")
        roles = service.list_roles_with_meta(prefix="persona-", required_tags=["cloud"])
    """

    def __init__(self, base_path: str):
        self.base_path = base_path

    @staticmethod
    def _get_title_from_readme(readme_path: str) -> str:
        """
        Extract the first Markdown H1 title from a README.md file.

        Args:
            readme_path (str): The path to the README.md file.

        Returns:
            str: The extracted title or None.
        """
        if not os.path.exists(readme_path):
            return None

        with open(readme_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip().startswith("# "):
                    return line.strip("# ").strip()
        return None

    def list_roles_with_meta(self, prefix: str = None, required_tags: list = None) -> dict:
        """
        List all roles with metadata, optionally filtered by prefix and required tags.

        Args:
            prefix (str, optional): Filter roles starting with this prefix.
            required_tags (list, optional): Filter roles that contain any of these tags.

        Returns:
            dict: Sorted dictionary of roles with their metadata.
        """
        roles = {}

        for role_name in os.listdir(self.base_path):
            if prefix and not role_name.startswith(prefix):
                continue

            role_path = os.path.join(self.base_path, role_name)
            meta_path = os.path.join(role_path, "meta", "main.yml")
            readme_path = os.path.join(role_path, "README.md")

            if not os.path.isdir(role_path) or not os.path.exists(meta_path) or not os.path.exists(readme_path):
                continue

            with open(meta_path, "r", encoding="utf-8") as file:
                meta = yaml.safe_load(file)

            tags = meta.get("galaxy_info", {}).get("galaxy_tags", [])

            if required_tags and not any(tag in tags for tag in required_tags):
                continue

            application_id = role_name[len(prefix):] if prefix else role_name
            title = self._get_title_from_readme(readme_path) or application_id.replace("-", " ").title()

            roles[role_name] = {
                "path": role_path,
                "meta": meta,
                "readme": readme_path,
                "title": title,
                "application_id": application_id,
            }

        return dict(sorted(roles.items()))
