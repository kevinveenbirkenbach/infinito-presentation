import os

def list_snippets(template_folder, subdir, suffix=".html.j2", relative_paths=True):
    """
    List all files in a given template subdirectory.

    Args:
        template_folder (str): The base template folder path.
        subdir (str): The subdirectory relative to the template folder.
        suffix (str, optional): Only include files ending with this suffix. Defaults to ".html.j2".
        relative_paths (bool, optional): If True, return full relative paths (subdir/filename).
                                         If False, return only the filename. Defaults to True.

    Returns:
        list: Sorted list of matching file paths or filenames.

    Raises:
        ValueError: If no matching files were found in the given subdirectory.
    """
    dir_path = os.path.join(template_folder, subdir)
    files = sorted([
        f for f in os.listdir(dir_path)
        if os.path.isfile(os.path.join(dir_path, f)) and f.endswith(suffix)
    ])

    if not files:
        raise ValueError(f"No files with suffix '{suffix}' found in '{dir_path}'")

    if relative_paths:
        return [os.path.join(subdir, f) for f in files]
    return files