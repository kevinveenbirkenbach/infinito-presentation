import os
from flask import url_for

def get_background(template_folder, file_path):
    """
    Returns the background image URL for a given template file.
    Raises an error if the background image does not exist.

    Args:
        template_folder (str): The base template folder path.
        file_path (str): The relative path of the template file.

    Returns:
        str: data-background-image attribute for Reveal.js.

    Raises:
        ValueError: If the corresponding background image is missing.
    """
    background_path = f"img/slides/backgrounds/{file_path}.png"
    static_file_path = os.path.join('static', background_path)

    if not os.path.exists(static_file_path):
        raise ValueError(f"Missing background image: '{static_file_path}' for template '{file_path}'")

    return f'data-background-image="{ url_for("static", filename=background_path) }" data-background-opacity="0.6"'