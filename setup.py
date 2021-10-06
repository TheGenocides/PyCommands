from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

setup(
    name="PyCommands",
    version="0.1.0",
    url="https://github.com/TheGenocides/PyCommands",
    description="A basic library to make custom commands in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="TheGenocide",
    author_email="luke.genesis.hyder@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords=[
        "pycommands",
        "PyCommands",
        "Pycomands"
    ],
    packages=find_packages(),
    install_requires=['colorama'],
)