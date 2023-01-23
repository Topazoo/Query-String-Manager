# :link: Query String Manager

 Simple Python utility to generate/parse URL query strings in standard or in Base64 format

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![PyPi](https://img.shields.io/badge/View%20On-PyPi-orange.svg)](https://pypi.org/project/Query-String-Manager/)

## Installation

```sh
$ pip install Query-String-Manager
```

## Quick Start

```python
$ python
Python 3.9.0 (default, Oct 27 2020, 14:15:17) 
[Clang 12.0.0 (clang-1200.0.32.21)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> from QueryStringManager import QueryStringManager

# Generate a standard query string from a dictionary

>>> QueryStringManager.generate_query_string({"str": "arg", "int": 1, "float": .01, "bool": True})
'?str=arg&int=1&float=0.01&bool=true'

# Parse a standard query string to a dictionary of Python objects

>>> QueryStringManager.parse_query_string('?str=arg&int=1&float=0.01&bool=true')
{'str': 'arg', 'int': 1, 'float': Decimal('0.01'), 'bool': True}


>>> QueryStringManager.parse('?str=arg&int=1&float=0.01&bool=true')
{'str': 'arg', 'int': 1, 'float': Decimal('0.01'), 'bool': True}

# Generate a base64 encoded query string from a dictionary

>>> QueryStringManager.generate_base64_query_string({"nested_dict": {"float": .1}, "list": [{"int": 1, "bool": True}]})
'?data=eyJuZXN0ZWRfZGljdCI6IHsiZmxvYXQiOiAwLjF9LCAibGlzdCI6IFt7ImludCI6IDEsICJib29sIjogdHJ1ZX1dfQ=='

# Parse a base64 encoded query string to a dictionary

>>> QueryStringManager.parse_base64_query_string('?data=eyJuZXN0ZWRfZGljdCI6IHsiZmxvYXQiOiAwLjF9LCAibGlzdCI6IFt7ImludCI6IDEsICJib29sIjogdHJ1ZX1dfQ==')
{'data': {'nested_dict': {'float': Decimal('0.1')}, 'list': [{'int': 1, 'bool': True}]}}

>>> QueryStringManager.parse('?data=eyJuZXN0ZWRfZGljdCI6IHsiZmxvYXQiOiAwLjF9LCAibGlzdCI6IFt7ImludCI6IDEsICJib29sIjogdHJ1ZX1dfQ==')
{'data': {'nested_dict': {'float': Decimal('0.1')}, 'list': [{'int': 1, 'bool': True}]}}
```

## Overview

This utility can be used easily manage query strings in Python. It allows standard query strings to be generated from Python dictionaries containing the following types (`str`, `int`, `float` `decimal.Decimal`, `bool`)

```python
>>> QueryStringManager.generate_query_string({"str": "arg", "int": 1, "float": .01, "bool": True})
'?str=arg&int=1&float=0.01&bool=true'
```

Similarly it can parse query strings into dictionaries of the same types (`float` will be replaced with `decimal.Decimal` to avoid narrowing/widening issues)

```python
>>> QueryStringManager.parse_query_string('?str=arg&int=1&float=0.01&bool=true')
{'str': 'arg', 'int': 1, 'float': Decimal('0.01'), 'bool': True}
```

More interestingly, this utility also allows the same functionality but with base64 encoded query strings. This allows more complex objects such as lists and nested dictionaries to be passed in a query string.

For example, a Javascript application could create the following complex query string and base64 encode it:  

```js
var obj = {nested: {a: 'a', b: 'b'}, list: [1, {"in": "list"}, true]};
"?data=" + btoa(JSON.stringify(obj));

'?data=eyJuZXN0ZWQiOnsiYSI6ImEiLCJiIjoiYiJ9LCJsaXN0IjpbMSx7ImluIjoibGlzdCJ9LHRydWVdfQ=='
```

And this library could be used to automatically decode this back to correctly typed objects in Python:

```python
>>> from QueryStringManager import QueryStringManager

>>> QueryStringManager.parse_base64_query_string('?data=eyJuZXN0ZWQiOnsiYSI6ImEiLCJiIjoiYiJ9LCJsaXN0IjpbMSx7ImluIjoibGlzdCJ9LHRydWVdfQ==')

{'data': {'nested': {'a': 'a', 'b': 'b'}, 'list': [1, {'in': 'list'}, True]}}
```

This library can also be used to generate these query strings directly:

```python
>>> from QueryStringManager import QueryStringManager

>>> QueryStringManager.generate_base64_query_string({'nested': {'a': 'a', 'b': 'b'}, 'list': [1, {'in': 'list'}, True]}, field_name="data")
'?data=eyJuZXN0ZWQiOiB7ImEiOiAiYSIsICJiIjogImIifSwgImxpc3QiOiBbMSwgeyJpbiI6ICJsaXN0In0sIHRydWVdfQ=='
```

For the cost of a tiny performance hit, the `parse()` method may be used to parse either a base64 encoded or normal format query string, or a query string with a mix of formats:

```python
>>> from QueryStringManager import QueryStringManager

>>> QueryStringManager.parse("?val2=false&y=eyJ0ZXN0MiI6IFsxLCAyLCAzXX0=")
{"val2": False, "y": {"test2": [1,2,3]}}
```

## Methods

### QueryStringManager.parse()

```python
parse(query_string:str)
```

<b>Arguments:</b>

- <i>query_string</i> - The query string to parse into a dictionary. A valid query string will use `"="` to seperate keys and values, like: `"?key=value"`. The `"?"` prefix is optional in query strings passed to this method.  

    The data in the query string may be in standard or in base64 format. This method will detect the encoding and parse it even if different fields may have different formats
  

    This method can generally be used in place of `parse_base64_query_string()` and `parse_query_string()` with the drawback of a slight performance hit checking each the encoding of each field in the query string. See these methods for details on parsing behavior when either format is present


<b>Returns:</b>

- <i>dict</i> - A dict containing the key/value pairs in the query string

<b>Exceptions:</b>

- <i>ValueError</i> - If the passed `query_string` does not have a valid format this exception will be thrown

### QueryStringManager.generate_query_string()

```python
generate_query_string(params:dict, safe_chars:str=None)
```

<b>Arguments:</b>

- <i>params</i> - A dictionary of key/value pairs to write to a query string. This dictionary must be flat and contain no sequences. In addition, the values in the dictionary must be one of the following types: (`str`, `int`, `float` `decimal.Decimal`,  `bool`). These are the only types that can be cleanly represented in a normal query string

<br>

- <i>safe_chars [optional]</i> - When the query string is generated, some characters will be replaced with URL safe characters (such as `" "` to `"%20"`). These characters are defined in RFC 3986 and the replacement is performed by [urllib.parse.quote](https://docs.python.org/3/library/urllib.parse.html#url-quoting). This library specifies some characters to not replace by default (`";/?!:@&=+$,."`). The `safe_chars` argument allows a custom string to be passed defining the characters that should not be replaced by URL safe equivalents

<b>Returns:</b>

- <i>str</i> - The generated query string

<b>Exceptions:</b>

- <i>ValueError</i> - If the constraints on <i>params</i> listed above are not met this exception will be thrown

### QueryStringManager.parse_query_string()

```python
parse_query_string(query_string:str, normalize_value:bool=True)
```

<b>Arguments:</b>

- <i>query_string</i> - The query string to parse into a dictionary. A valid query string will use `"="` to seperate keys and values, like: `"?key=value"`. The `"?"` prefix is optional in query strings passed to this method. By default, sequences `urllib` detects were replaced for URL safety will be converted to their normal equivalent (such as `"%20"` to `" "`)

<br>

- <i>normalize_value [optional]</i> - By default, data in the query string will be converted to its detected Python type. For example a value of `"1"` in the string will be interpreted as an `int`. `"3.14"` will be interpreted as a `decimal.Decimal` and `false`/`true` will be replaced with a `bool`. Setting `normalize_value` to `False` will disable this and all values will be interpreted as strings

<b>Returns:</b>

- <i>dict</i> - A dict containing the key/value pairs in the query string

<b>Exceptions:</b>

- <i>ValueError</i> - If the passed `query_string` does not have a valid format this exception will be thrown

### QueryStringManager.generate_base64_query_string()

```python
generate_base64_query_string(params:Union[int, str, bool, float, Decimal, list, dict], field_name:str="q")
```

<b>Arguments:</b>

- <i>params</i> - An individual value of a serializable type (`str`, `int`, `float` `decimal.Decimal`, `bool`), a dictionary (can be nested), list, or any combination of these types valid in Python. This means that non-dict types can be encoded:

  <br>

    ```python
    >>> QueryStringManager.generate_base64_query_string(3.14)
    '?q=My4xNA=='

    >>> QueryStringManager.generate_base64_query_string(True)
    '?q=dHJ1ZQ=='
    ```

  It also means lists can be encoded directly, as can nested dicts:
  
  <br>

    ```python
    >>> QueryStringManager.generate_base64_query_string([1,2,3])
    '?q=WzEsIDIsIDNd'

    >>> QueryStringManager.generate_base64_query_string({"nested": {"one": {"two": "deep"}}})
    '?q=eyJuZXN0ZWQiOiB7Im9uZSI6IHsidHdvIjogImRlZXAifX19'

    >>> QueryStringManager.generate_base64_query_string([{"dict": 1}])
    '?q=W3siZGljdCI6IDF9XQ=='
    ```

  <br>

- <i>field_name [optional]</i> - The name of the field that should contain the encoded data. The default is `"q"`, creating a query string like `"q=<base64 encoded data>"`. If field_name is overridden to something like `"data"` the resulting query string would look like `"data=<base64 encoded data>"`

<b>Returns:</b>

- <i>str</i> - The generated base64 encoded query string

<b>Exceptions:</b>

- <i>ValueError</i> - If the type constraints on <i>params</i> listed above are not met this exception will be thrown

### QueryStringManager.parse_base64_query_string()

```python
parse_base64_query_string(query_string:str)
```

<b>Arguments:</b>

- <i>query_string</i> - The base64 encoded query string to parse into a dictionary. The passed query string may contain multiple fields and base64 values (seperated by `"&"`), but all must be base64 encoded. The fields will be the top level keys in the dictionary, and the values will be supported Python objects (`str`, `int`, `float` `decimal.Decimal`, `bool`). The following are examples of decoded query strings:

    <br>

    ```python
    >>> QueryStringManager.parse_base64_query_string('?q=My4xNA==&test=dHJ1ZQ==&data=WzEsIDIsIDNd')
    {'q': Decimal('3.14'), 'test': True, 'data': [1, 2, 3]}

    >>> QueryStringManager.parse_base64_query_string('?q=eyJuZXN0ZWQiOiB7Im9uZSI6IHsidHdvIjogImRlZXAifX19')
    {'q': {'nested': {'one': {'two': 'deep'}}}}

    >>> QueryStringManager.parse_base64_query_string('?q=W3siZGljdCI6IDF9XQ==')
    {'q': [{'dict': 1}]}
    ```

<b>Returns:</b>

- <i>dict</i> - A dict containing the key/value pairs in the query string

<b>Exceptions:</b>

- <i>ValueError</i> - If the passed `query_string` does not have a valid format this exception will be thrown

## Contributing

- Contributions are welcome! Please not the following when contributing:
  - Unittests must be added under the `tests/` directory for the PR to be approved. You can run unittests from the root project directory with the following command:

    ```sh
    $ python -m unittest discover -s tests -p test*.py
    ```

  - PRs cannot be merged without all unittests passing (they will execute automatically)
  - Merges to `main` will automatically create a new release on PyPi
