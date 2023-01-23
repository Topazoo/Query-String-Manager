from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Query-String-Manager',
    version='0.1',
    description='Simple Python utility to generate/parse URL query strings, either raw or in Base64 format',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Topazoo/Query-String-Manager',
    project_urls={
        'Bug Tracker': 'https://github.com/Topazoo/Query-String-Manager/issues',
        'Changelog': 'https://github.com/Topazoo/Query-String-Manager/releases',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers"
    ],
    package_dir={'':'query_string_manager'},
    packages=find_packages(where='query_string_manager'),
    python_requires='>=3.6',
)
