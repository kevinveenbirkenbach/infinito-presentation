# utils/base_config_loader.py

import os
import yaml


class BaseConfigLoader:
    """
    Base class for loading YAML configuration files.

    Usage:
        loader = BaseConfigLoader("config.yml")
        value = loader.get("my_key", "default_value")
    """

    def __init__(self, config_path: str):
        self._config_path = config_path
        self._config_data = self._load_config()

    def _load_config(self) -> dict:
        if not os.path.exists(self._config_path):
            raise FileNotFoundError(f"Config file not found: {self._config_path}")

        with open(self._config_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def get(self, key: str, default=None):
        return self._config_data.get(key, default)
