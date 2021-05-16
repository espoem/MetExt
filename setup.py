import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")
requirements = (here / "requirements.txt").read_text(encoding="utf-8")

about = {}
exec((here / "metext/__version__.py").read_text(encoding="utf-8"), about)

setup(
    name="metext",
    version=about["__version__"],
    description="A tool to find data patterns in potentially encoded binary data",
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
)
