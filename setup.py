import io
import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with io.open(os.path.join(HERE, "README.md"), "rt", encoding="utf8") as f:
        return f.read()


def load_about():
    about = {}
    with io.open(
        os.path.join(HERE, "tutorenterprisecatalog", "__about__.py"),
        "rt",
        encoding="utf-8",
    ) as f:
        exec(f.read(), about)  # pylint: disable=exec-used
    return about


ABOUT = load_about()


setup(
    name="tutor-contrib-enterprisecatalog",
    version=ABOUT["__version__"],
    url="https://github.com/Dicey-Tech/tutor-contrib-enterprisecatalog",
    project_urls={
        "Code": "https://github.com/Dicey-Tech/tutor-contrib-enterprisecatalog",
        "Issue tracker": "https://github.com/Dicey-Tech/tutor-contrib-enterprisecatalog/issues",
    },
    license="AGPLv3",
    author="Sofiane Bebert",
    description="enterprise-catalog plugin for Tutor",
    long_description=load_readme(),
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=["tutor>=16.0.0,<17.0.0"],
    extras_require={"dev": "tutor[dev]>=16.0.0,<17.0.0"},
    python_requires=">=3.8",
    entry_points={
        "tutor.plugin.v1": [
            "enterprise-catalog = tutorenterprisecatalog.plugin"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
