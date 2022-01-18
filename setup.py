# command to install PygameHaze from test.pypi and pypi at the same time:
# windows: py -pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ PygameHaze
# Unix/macOS: python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ PygameHaze

from setuptools import setup, find_packages
import PygameHaze as target_package
from pathlib import Path
import platform
import sys
import os


def consume_args(arg: str):
    if arg in sys.argv:
        sys.argv.remove(arg)
        return True
    return False


ROOT = Path(__file__).parent
README_FILE = [ROOT / file for file in os.listdir(ROOT) if file.startswith("README")][0]

long_description = "\n" + README_FILE.read_text(encoding="utf-8")

PACKAGE_NAME = target_package.__name__
VERSION = target_package.__version__
AUTHOR = target_package.__author__
DESCRIPTION = "helpful tools/widgets for pygame"

requirements = [line.strip() for line in (ROOT / "requirements.txt").read_text().splitlines()]

full = consume_args("--full")


if consume_args("-format") or full or 1:
    try:
        import black
    except ImportError:
        print("you need to have black installed to format your code")
        if platform.system() == "Windows":
            print("pip install black")
        else:
            print("python3 -m pip install black")
        sys.exit(1)

    import glob
    print("formatting with black...")

    python_folders = [
        ROOT / "PygameHaze",
        ROOT / "Examples",
    ]

    for filepath in (
            file
            for directory in python_folders
            for file in glob.iglob(f"{directory}/**/*.py", recursive=True)
    ):
        path = Path(os.getcwd(), filepath)
        if black.format_file_in_place(
            path, False, black.FileMode(), black.WriteBack.YES
        ):
            print(f"Formatted file: {filepath}")
        else:
            print(f"Skipping file {filepath} as it is already formatted")

    print("finished formatting")
    sys.exit(0)


def setup_package():
    metadata = {
        "name": PACKAGE_NAME,
        "version": VERSION,
        "author": AUTHOR,
        "author_email": "emc235.dev@gmail.com",
        "description": DESCRIPTION,
        "long_description": long_description,
        "long_description_content_type": "text/markdown",
        "url": "https://github.com/Emc2356/PygameHaze",
        "packages": find_packages(),
        "python_requires": ">=3.7",
        "license": "MIT",
        "install_requires": requirements
    }

    setup(**metadata)


if __name__ == '__main__':
    setup_package()
