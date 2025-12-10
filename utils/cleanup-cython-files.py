import os


def remove_cython_build_files(root_dir):
    """
    Removes .pyx and .c files from the specified root directory and its subdirectories.

    Args:
        root_dir (str): The path to the root directory to clean.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".pyx") or filename.endswith(".c") or filename.endswith(".so"):
                file_path = os.path.join(dirpath, filename)
                try:
                    os.remove(file_path)
                    print(f"Removed: {file_path}")
                except OSError as e:
                    print(f"Error removing {file_path}: {e}")


if __name__ == "__main__":
    # Specify the directory to clean.
    # For example, to clean the current directory:
    # directory_to_clean = "."
    # Or a specific path:
    directory_to_clean = "./caqui"

    if os.path.exists(directory_to_clean):
        remove_cython_build_files(directory_to_clean)
    else:
        print(f"Error: Directory '{directory_to_clean}' not found.")
