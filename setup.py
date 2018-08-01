from setuptools import setup

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="qiwi_api",
    version="1.0",

    author="Helow19274",
    author_email="helow@helow19274.tk",

    description="Qiwi api wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/helow19274/qiwi_api",
    packages=['qiwi_api'],
    install_requires=['requests'],

    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    )
)
