from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

PACKAGE_NAME = "PygameWidgets"
VERSION = "0.1.1"
DESCRIPTION = "Some widgets for pygame"

# Setting up
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="emc235",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Emc2356/Pygame-Widgets",
    packages=find_packages(),
    python_requires=">=3.6",
    license="MIT",
    install_requires=["pygame"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent'
    ]
)
