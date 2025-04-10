import os
import yaml
import re

def get_title_from_readme(readme_path):
    if not os.path.exists(readme_path):
        return None

    with open(readme_path, "r", encoding="utf-8") as f:
        for line in f:
            # Look for first Markdown H1
            if line.strip().startswith("# "):
                return line.strip("# ").strip()
    return None


def list_roles_with_meta(base_path, prefix=None, required_tags=None):
    roles = {}

    for role_name in os.listdir(base_path):
        if prefix and not role_name.startswith(prefix):
            continue

        role_path = os.path.join(base_path, role_name)
        meta_path = os.path.join(role_path, "meta", "main.yml")
        readme_path = os.path.join(role_path, "README.md")

        if not os.path.isdir(role_path):
            continue
        if not os.path.exists(meta_path):
            continue
        if not os.path.exists(readme_path):
            continue

        with open(meta_path, "r", encoding="utf-8") as f:
            meta = yaml.safe_load(f)

        tags = meta.get("galaxy_info", {}).get("galaxy_tags", [])

        if required_tags:
            if not any(tag in tags for tag in required_tags):
                continue

        # Determine title
        title = get_title_from_readme(readme_path)
        if not title:
            # Fallback: role_name without prefix
            title = role_name[len(prefix):] if prefix else role_name
            title = title.replace("-", " ").title()

        roles[role_name] = {
            "path": role_path,
            "meta": meta,
            "readme": readme_path,
            "title": title,
        }

    return dict(sorted(roles.items()))
