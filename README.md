# Query String Manager
 Simple Python utility to generate/parse URL query strings in standard or in Base64 format

[![PyPi](https://img.shields.io/badge/View%20On-PyPi-orange.svg)](https://pypi.org/project/Query-String-Manager/)


## Installation:
```sh
$ pip install Query-String-Manager
```

## Quick Start:
```python
$ python
Python 3.9.0 (default, Oct 27 2020, 14:15:17) 
[Clang 12.0.0 (clang-1200.0.32.21)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> from query_string_manager import QueryStringManager

# Generate a standard query string from a dictionary

>>> QueryStringManager.generate_query_string({"str": "arg", "int": 1, "float": .01, "bool": True})
'?str=arg&int=1&float=0.01&bool=true'

# Parse a standard query string to a dictionary of Python objects

>>> QueryStringManager.parse_query_string('?str=arg&int=1&float=0.01&bool=true')
{'str': 'arg', 'int': 1, 'float': Decimal('0.01'), 'bool': True}

# Generate a base64 encoded query string from a dictionary

>>> QueryStringManager.generate_base64_query_string({"nested_dict": {"float": .1}, "list": [{"int": 1, "bool": True}]})
'?data=eyJuZXN0ZWRfZGljdCI6IHsiZmxvYXQiOiAwLjF9LCAibGlzdCI6IFt7ImludCI6IDEsICJib29sIjogdHJ1ZX1dfQ=='

# Parse a base64 encoded query string to a dictionary

>>> QueryStringManager.parse_base64_query_string('?data=eyJuZXN0ZWRfZGljdCI6IHsiZmxvYXQiOiAwLjF9LCAibGlzdCI6IFt7ImludCI6IDEsICJib29sIjogdHJ1ZX1dfQ==')
{'data': {'nested_dict': {'float': Decimal('0.1')}, 'list': [{'int': 1, 'bool': True}]}}
```

## Overview:

## Methods:

#### QueryStringManager.generate_query_string()

#### QueryStringManager.parse_query_string()

#### QueryStringManager.generate_base64_query_string()

#### QueryStringManager.parse_base64_query_string()

## Contributing:
