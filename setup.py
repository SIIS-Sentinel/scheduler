from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="scheduler",
    version="0.1.0",
    author="Adrien Cosson",
    author_email="adrien@cosson.io",
    description="The Scheduler code for the Sentinel experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/AdrienCos/scheduler",
    packages=find_packages(),
    install_requires=[
        'paho-mqtt'
    ],
    python_requires=">=3.5"
)
