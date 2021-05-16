import os
import pathlib
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")
requirements = (here / "requirements.txt").read_text(encoding="utf-8")

about = {}
exec((here / "metext/__version__.py").read_text(encoding="utf-8"), about)


class UploadCommand(Command):
    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("-> {0}".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(str(here / "dist"), ignore_errors=True)
            rmtree(str(here / "build"), ignore_errors=True)
            rmtree(str(here / "metext.egg-info"), ignore_errors=True)
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine...")
        os.system("twine upload dist/*")

        self.status("Pushing git tags...")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


class UploadTestCommand(UploadCommand):
    description = "Build and publish the package to test environment."
    user_options = []

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(str(here / "dist"), ignore_errors=True)
            rmtree(str(here / "build"), ignore_errors=True)
            rmtree(str(here / "metext.egg-info"), ignore_errors=True)
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to test PyPI via Twine...")
        os.system("twine upload --repository testpypi dist/*")

        sys.exit()


setup(
    name="metext",
    version=about["__version__"],
    description="A tool to search for data patterns in (encoded) binary data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    packages=find_packages(exclude=["tests"]),
    install_requires=requirements,
    include_package_data=True,
    entry_points={"console_scripts": ["metext=cli:main"]},
    python_requires=">=3.5",
    license="LGPLv3+",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Programming Language :: Python :: 3",
    ],
    url="https://github.com/espoem/MetExt",
    project_urls={
        "Source": "https://github.com/espoem/MetExt",
        "Tracker": "https://github.com/espoem/MetExt/issues",
    },
    cmdclass={"upload": UploadCommand, "tupload": UploadTestCommand},
)
