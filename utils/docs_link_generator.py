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

def generate_docs_link(source_path: str) -> str:
    """
    Generate a documentation link based on the given source path.

    This function replaces the '/source/' prefix with the base URL defined in the configuration
    and converts Markdown (.md) file extensions to HTML (.html).

    Args:
        source_path (str): The source file path (e.g., '/source/docs/overview/Problem_Statement.md').

    Returns:
        str: The generated documentation link.
    """
    # Get the base URL for documentation from configuration
    docs_base_url = config.get("docs_base_url", "/docs/")
    # Ensure that the base URL ends with a trailing slash
    if not docs_base_url.endswith("/"):
        docs_base_url += "/"

    # Convert Markdown file extension to HTML if applicable
    if source_path.endswith(".md"):
        source_path = source_path[:-3] + ".html"

    # Remove the '/source/' prefix from the path if it exists
    if source_path.startswith("/source/"):
        source_path = source_path[len("/source/"):]

    # Generate the full link by concatenating the base URL and the modified source path
    link = docs_base_url + source_path
    return link

# Example usage
if __name__ == "__main__":
    example_path = "/source/docs/overview/Problem_Statement.md"
    print("Generated Link:", generate_docs_link(example_path))
