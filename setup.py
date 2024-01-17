#!/usr/bin/env python
# coding=utf-8
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='df-csv-excel',
    version='0.1.6',
    author="ZhangLe",
    author_email="zhangle@gmail.com",
    description="Commonly used functions for Data Scientists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cheerzhang/read_csv_excel",
    project_urls={
        "Bug Tracker": "https://github.com/cheerzhang/read_csv_excel/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages("."),
    install_requires=[
        'pandas>=0.25.1',
        'numpy>=1.21.5',
        'plotly >= 5.18.0'
    ],
    python_requires=">=3.9",
)
