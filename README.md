# eol_python
A Python 3 wrapper for the [Encyclopedia of Life API](http://eol.org/api).

## Installation
Clone this repo and import eol_api_wrapper.py as a module:

 ```python 
 >>> import eol_api_wrapper as eol
 ```

## Usage
To start accessing the API, first instantiate an instance of the API class. If you intend to make a lot of calls to the API, generate an API key as described [here](http://eol.org/info/api_overview) and add as an argument:

```python
>>> api = eol.API(key= 12345)
```

Check whether you can ping the api:

```python
>>> api.ping()
#'Success'
```

You now have access to the EOL API methods `Page`, `Search`, `Collections`, `DataObjects` and `HierachyEntries` from within the `api` object:

```python
>>> page = api.Page(1045608)
>>> page.scientific_name #returned variables are stored as object attributes
#'Apis mellifera Linnaeus 1758'
```

Each method returns a JSON object. Specific method arguments can be adjusted using `**kwargs`.

The `Search` method comes with an added optional `"all"` argument that returns all the pages for a particular search string.

```python
>>> marchantia = api.Search("Marchantia",page = "all") 
>>> marchantia.total_results
#167
>>> len(marchantia.results)
#167
```




