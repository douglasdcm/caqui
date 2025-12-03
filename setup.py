from distutils.core import setup

from Cython.Build import cythonize
from setuptools import setup

setup(
    ext_modules=cythonize(
        [
            "./caqui/asynchronous.pyx",
            "./caqui/constants.pyx",
            "./caqui/helper.pyx",
            "./caqui/exceptions.pyx",
            "./caqui/cssify.pyx",
            "./caqui/synchronous.pyx",
            "./caqui/by.pyx",
            "./caqui/__init__.pyx",
            "./caqui/easy/capabilities.pyx",
            "./caqui/easy/options.pyx",
            "./caqui/easy/action_chains.pyx",
            "./caqui/easy/alert.pyx",
            "./caqui/easy/page.pyx",
            "./caqui/easy/switch_to.pyx",
            "./caqui/easy/window.pyx",
            "./caqui/easy/element.pyx",
            "./caqui/easy/__init__.pyx",
            "./caqui/easy/server.pyx",
        ],
        compiler_directives={
            "language_level": 3,
            "boundscheck": False,
            "wraparound": False,
            "cdivision": True,
            "initializedcheck": False,
            "nonecheck": False,
        },
    ),
)
