from setuptools import find_packages, setup

setup(
    name="torrentseeker",
    version="0.0.1",
    description="torrentseeker - find torrents using different resources.",
    author="David Linn",
    author_email="wujiocean@protonmail.com",
    packages=find_packages(exclude=("tests",)),
    install_requires=["aiohttp", "python-dateutil", "BeautifulSoup4", "click"],
    entry_points={
        "console_scripts": [
            "torrentseeker-cli = torrentseeker.cli:cli",
        ]
    },
)
