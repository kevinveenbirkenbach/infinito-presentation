import os
from utils.base_config_loader import BaseConfigLoader


class AppUrlService(BaseConfigLoader):
    """
    Service class for generating application URLs based on configuration.

    Usage:
        service = AppUrlService("config.yml")
        url = service.generate_url("nextcloud")
    """

    def __init__(self, config_path: str):
        super().__init__(config_path)

    def generate_url(self, application_id: str) -> str:
        """
        Generate a URL for a given application ID.

        Args:
            application_id (str): The application identifier (e.g., 'nextcloud').

        Returns:
            str: The generated URL (e.g., 'https://nextcloud.example.com/').
        """
        domain = self.get("app_domain", "yourdomain.com")
        return f"https://{application_id}.{domain}/"
