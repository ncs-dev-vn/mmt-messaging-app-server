"""
Cấu hình thiết lập cho Messaging Server
"""

from setuptools import setup, find_packages

with open("doc/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="messaging-server",
    version="1.0.0",
    author="MMT Project Team",
    description="A simple and robust Python messaging server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Chat",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "mmt-server=main:main",
        ],
    },
)