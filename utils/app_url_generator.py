import os
import yaml

# Define the path to the configuration file relative to this module
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "../config.yml")

def load_config():
    """Load configuration from the YAML file."""
    with open(CONFIG_FILE, "r", encoding="utf-8") as config_file:
        return yaml.safe_load(config_file)

# Load the configuration globally
config = load_config()

def generate_app_url(application_id: str) -> str:
    """
    Generate a URL for the software based on the given application ID.
    
    The generated URL will be of the format:
      https://{application_id}.{app_domain}/
      
    The app_domain is retrieved from the configuration file.
    
    Args:
        application_id (str): The identifier of the application.
    
    Returns:
        str: The generated URL for the software.
    """
    # Get the app domain from the configuration, defaulting to "yourdomain.com"
    app_domain = config.get("app_domain", "yourdomain.com")
    # Generate the full URL
    url = f"https://{application_id}.{app_domain}/"
    return url

# Example usage:
if __name__ == "__main__":
    example_application_id = "docker-app"
    print("Generated URL:", generate_app_url(example_application_id))
