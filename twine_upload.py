import subprocess
import dotenv
import sys
import os


TEST_PYPI = True


def build():
    if os.path.exists("dist"):
        print("[LOG] no dist file was found so we are attempting to build from setup.py")
        # delete files that might exist
        for cmd in [
            "del dist\ *.* / s / q",
            "del build\ *.* / s / q",
            "del PygameHaze.egg - info\ *.* / s / q"
        ]:
            try: subprocess.call(cmd)
            except FileNotFoundError: pass
    print("[LOG] building the package...")
    subprocess.call(f"{sys.executable} setup.py sdist bdist_wheel")  # do the actual build


def upload():
    dotenv.load_dotenv()
    USERNAME = os.environ["PYPI_USERNAME"]
    PASSWORD = os.environ["PYPI_PASSWORD"]

    try:
        import twine
    except ImportError:
        print("couldn't locate twine, maybe it isnt installed?")
        sys.exit(1)

    print("[LOG] uploading the package...")
    if TEST_PYPI:
        subprocess.call(f"{sys.executable} -m twine upload --repository testpypi dist/* -u {USERNAME} -p {PASSWORD}")
    else:
        pass
        # subprocess.call(f"{sys.executable} -m twine upload dist/* -u {USERNAME} -p {PASSWORD}")


if __name__ == '__main__':
    if (
            "-h" in sys.argv or
            "-help" in sys.argv or
            "--h" in sys.argv or
            "--help" in sys.argv
    ):
        print("a helper script to build and upload to pypi with twine")
        print("--nobuild it doesnt build the project again before it uploads")
        exit()
    if "--nobuild" not in sys.argv:
        build()
    upload()
