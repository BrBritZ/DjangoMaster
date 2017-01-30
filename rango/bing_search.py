import json
import urllib, urllib2 # Py2.7.x
from py_ms_cognitive import PyMsCognitiveWebSearch

# Add your Microsoft Account Key to a file called bing.key

def read_bing_key():
    """
    Reads the BING API key from a file called 'bing.key'.
    returns: a string which is either None, i.e. no key found, or with a key.
    Remember: put bing.key in your .gitignore file to avoid committing it!
    """
    # See Python Anti-Patterns - it's an awesome resource!
    # Here we are using "with" when opening documents.
    # http://docs.quantifiedcode.com/python-anti-patterns/maintainability/
    bing_api_key = None

    try:
        with open('bing.key','r') as f:
            bing_api_key = f.readline()
    except:
        raise IOError('bing.key file not found')

    return bing_api_key

def run_query(search_terms):
    """
    Given a string containing search terms (query),
    returns a list of results from the Bing search engine.
    """
    bing_api_key = read_bing_key()

    if not bing_api_key:
        raise KeyError("Bing Key Not Found")

    search_service = PyMsCognitiveWebSearch(bing_api_key, search_terms)
    results = search_service.search(limit=50, format='json')
    print(results[0])

    # Return the list of results to the calling function.
    return results