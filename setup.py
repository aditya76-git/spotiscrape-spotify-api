import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spotiscrape",
    version="1.0.0",
    author="aditya76-git",
    author_email="cdr.aditya.76@gmail.com@gmail.com",
    description="SpotiScrape - SPOTIFY API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aditya76-git/spotiscrape-spotify-api",
    project_urls={
        "Tracker": "https://github.com/aditya76-git/spotiscrape-spotify-api/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "pybase62",
        "pytz"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)