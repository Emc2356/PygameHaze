from setuptools import setup, find_packages
import PygameHelper as pgh
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

PACKAGE_NAME = "PygameHelper"
VERSION = pgh.__version__
DESCRIPTION = "helpful tools/widgets for pygame"


def setup_package():
    metadata = {
        "name": PACKAGE_NAME,
        "version": VERSION,
        "author": "emc235",
        "description": DESCRIPTION,
        "long_description": long_description,
        "long_description_content_type": "text/markdown",
        "url": "https://github.com/Emc2356/PygameHelper",
        "packages": find_packages(),
        "python_requires": ">=3.7",
        "license": "MIT",
        "install_requires": ["pygame", "numpy"]
    }

    setup(**metadata)


if __name__ == '__main__':
    setup_package()
