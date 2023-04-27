import os
import setuptools

from doctree import __version__


readme_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
with open(readme_filepath, "r") as fh:
    long_description = fh.read()


extras_require_packages = {
    "dev": ["pytest", "coverage", "black", "flake8"],
    "demo": [
        "jinja2",
        "uvicorn",
        "fastapi",
        "python-multipart",
    ],
}
extras_require_packages["all"] = (
    extras_require_packages["dev"] + extras_require_packages["demo"]
)


setuptools.setup(
    name="pytorch-doctree",
    version=__version__,
    author="Tong Zhu",
    author_email="tzhu1997@outlook.com",
    description="A toolkit for text segment concatenation and doc tree construction",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=setuptools.find_packages(
        exclude=["tests", "tests.*", "docs", "docs.*", "data"]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "omegaconf>=2.0.6",
        "tqdm>=4.61.1",
        "pytorch-rex==0.0.15",
        "lxml>=4.6.3",
        "transformers>=4.12.5",
    ],
    extras_require=extras_require_packages,
)
