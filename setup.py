try:
        from setuptools import setup
except:
        from distutils.core import setup

dist = setup(
    name = 'persistent-lru-cache',
    version = '0.1.0',
    description = "Adds a persistent_lru_cache decorator, like functools.lru-cache but persistent.",
    
    long_description = """
        persistent_lru_cache works exactly like functools.lru-cache,
        except that it takes an extra `filename` parameter, and persists
        the cache across runs.""",
        
    author = 'Andrew Barnert',
    author_email = 'abarnert@yahoo.com',
    url = 'http://github.com/abarnert/persistent-lru-cache/',
    license = 'MIT',
    classifiers = [     
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords = 'python functional',    
    modules = ['persistent_lru_cache'],
)
