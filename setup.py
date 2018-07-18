import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="generalmap",
    version="1.0.0",
    author="Tidues Wei",
    author_email="tidues@gmail.com",
    description="A generalized map function for lift function over structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tidues/GeneralMap",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

