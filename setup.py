from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import os

# Collect all .pyx files
def list_pyx_files(base_dir):
    pyx_files = []
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith(".pyx"):
                pyx_files.append(os.path.join(root, f))
    return pyx_files

pyx_modules = list_pyx_files("caqui")

extensions = [
    Extension(
        module_path.replace("/", ".")[:-4],  # convert path → package.module
        [module_path],
    )
    for module_path in pyx_modules
]

setup(
    name="caqui",
    version="4.0.0",
    packages=find_packages(),
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": 3,
            "boundscheck": False,
            "wraparound": False,
            "cdivision": True,
            "initializedcheck": False,
            "nonecheck": False,
        },
    ),
    install_requires=[
        "requests",
        "aiohttp",
        "webdriver-manager",
        "types-requests",
        "orjson",
    ],
)
