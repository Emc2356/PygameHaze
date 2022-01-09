from setuptools import setup, find_packages
import PygameHazel as pgh
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

PACKAGE_NAME = "PygameHazel"
VERSION = pgh.__version__
DESCRIPTION = "helpful tools/widgets for pygame"

with codecs.open(os.path.join(here, "requirements.txt"), encoding="utf-8") as fh:
    requirements = fh.read().split()


def setup_package():
    metadata = {
        "name": PACKAGE_NAME,
        "version": VERSION,
        "author": "emc235",
        "author_email": "emc235.dev@gmail.com",
        "description": DESCRIPTION,
        "long_description": long_description,
        "long_description_content_type": "text/markdown",
        "url": "https://github.com/Emc2356/PygameHazel",
        "packages": find_packages(),
        "python_requires": ">=3.7",
        "license": "MIT",
        "install_requires": requirements
    }

    setup(**metadata)


if __name__ == '__main__':
    setup_package()
