from setuptools import setup, find_packages

setup(
    name="cli-search-tool",
    version="0.1",
    packages=find_packages(),
    package_dir={"": "."},
    install_requires=[
        "pathspec",  # GitignoreParserが依存
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "cli-search=src.main:main",
        ],
    },
)
