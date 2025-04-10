import os
import yaml

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

        roles[role_name] = {
            "path": role_path,
            "meta": meta,
            "readme": readme_path,
        }

    return dict(sorted(roles.items()))