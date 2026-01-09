import os
import shutil
import subprocess


def convert_python_to_pyx(root_folder: str):
    """
    Scans all subfolders of `root_folder` for .py files,
    copies each next to the original file with a .pyx extension,
    overwriting existing copies.
    """
    result = []
    for current_path, _, files in os.walk(root_folder):
        for filename in files:
            if filename.endswith(".py"):
                original_file = os.path.join(current_path, filename)
                pyx_filename = filename[:-3] + ".pyx"  # change extension
                pyx_path = os.path.join(current_path, pyx_filename)

                # Copy and overwrite
                shutil.copyfile(original_file, pyx_path)
                result.append(pyx_path)

    setup_py_content = (
        f"""
from setuptools import setup, find_packages
# from distutils.core import setup
try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False

setup(
    name="caqui",
    version="5.0.0",
    packages=find_packages(include=['caqui']),
    setup_requires=[
        "requests",
        "aiohttp",
        "webdriver_manager",
        "types-requests",
        "json",
        "Cython",
    ],
    ext_modules=cythonize(
        {result},
        """
        """
        compiler_directives={
            'language_level': 3,
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True,
            'initializedcheck': False,
            'nonecheck': False,
        },
    ),
)

"""
    )
    with open("setup.py", "w") as f:
        f.write(setup_py_content)


def build_pyx():
    # Run a simple command and capture output
    result = subprocess.run(
        ["python", "setup.py", "build_ext", "--inplace"],
        capture_output=True,
        text=True,
        check=True,
    )
    print("Stdout:", result.stdout)
    print("Stderr:", result.stderr)


if __name__ == "__main__":
    target_folder = "./caqui"
    convert_python_to_pyx(target_folder)
    build_pyx()
