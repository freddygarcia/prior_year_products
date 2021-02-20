
# Getting started

This script gather data from 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html' site.
The logic is stored in the models.py file and the implementation in the main.py and pw_shell files.


## Give a try!

Please install the dependencies in the requirements.txt file using the `pip install -r requirements` command (better use a virtual environment).
Run the implementation script with `python main.py`
The main.py script should display the search result as a json and also download documents in this folder.
The pw_shell.py file is a bash utility to use the library in the command line


## Command line examples

- Get json from form names:
    python pw_shell.py json -f "Form 100" "Form W-2"
    python pw_shell.py json --form_names "Form 100" "Form W-2"

- Download form pdf:
    python pw_shell.py download -f "Form 100" -yt 2020 -yf 2015
    python pw_shell.py download -f "Form W-2" --year-from 2012 --year-to 2019


# Development Details

## Python version

```
python >= 3.8.5
```


## Dependencies

```
beautifulsoup4==4.9.3
bs4==0.0.1
pandas==1.2.2
requests==2.25.1
```

## Development time

About 4 hours.


## Some notes:

The task was straightforward. The steps to get the task done from the easiest to the hardest:

1. parsing the html table to a dict
2. handle pagination
3. downloading the docs
4. grouping the data using pandas to get the min and max year per form
5. waiting for you to like the result :)


## To consider:

- I'm using type hints so it's easier to undestand the args and output of all methods.
- I try to respect most of Python coding conventions
- The solution uses POO approach 
