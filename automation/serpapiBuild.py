"""
UQO group publications from Google Scholar with SerpApi

Code to:

- Pull set of Google Scholar profiles via SerpApi (requires author to have a Google Scholar profile & ID).
- Amalgamate lists & remove duplicates.
- Write to JSON.

TODO:
- Write to HTML (in progress).
- API KEY passing/setting.


SerpAPI details:

- [Guide](https://serpapi.com/google-scholar-author-api)
- [Playground](https://serpapi.com/playground?engine=google_scholar_author)
- [Pypi](https://pypi.org/project/google-search-results/)


22/09/21    v1 testing

"""

#*** Imports
import json
import io
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime as dt

import pandas as pd

from boltons.iterutils import remap

# Basic routine from https://serpapi.com/playground?engine=google_scholar_author&author_id=IDU7HMMAAAAJ&hl=en&sort=pubdate
from serpapi import GoogleSearch

# Set globals - use just for API_KEY.
API_KEY = None
# authors = None

#*************** Global settings for authors
def getAPIkey(fileIn = 'API_KEY.txt'):
    """Load SerpAPI key from file."""
    global API_KEY
    # Read API key from file
    try:
        with open(fileIn,'r') as fileIn:
            API_KEY = fileIn.read().strip()

    except:
        print(f'*** ERROR: no API_KEY.txt file found at {fileIn}. To get an API Key, sign up at https://serpapi.com/.')

    return API_KEY

def setAuthors(fileIn = 'authors.json', urlBase = 'https://scholar.google.com/citations?user='):
    """Load authors (& IDs) from json file."""
    try:
        with open(fileIn) as fp:
            authors = json.load(fp)
    except:
        print(f'*** ERROR: no authors.json file found at {fileIn}.')

    # Set individual pages
    for k,item in authors.items():
        if authors[k]['ID'] is not None:
            authors[k]['URL'] = urlBase + authors[k]['ID']

    return authors


#*************** Get data from Google via SerpApi
def authorSearch(ID):
    """Pull articles for specified Google Scholar ID"""

    params = {
      "engine": "google_scholar_author",
      "hl": "en",
      "author_id": ID,
      "sort": "pubdate",
      "num": "100",     # Note max number of results returned == 100
      "api_key": API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    return search, results

def getAuthors(authors):
    """Search & return for all authors"""

    for k,item in authors.items():
        if authors[k]['ID'] is not None:
            search, results = authorSearch(authors[k]['ID'])

            authors[k]['search'] = search
            authors[k]['results'] = results

    return authors


#*************** Data processing
def DictListUpdate(lis1, lis2):
    """
    Quick list of dicts combiner, with duplicates skipped, from https://stackoverflow.com/a/9891074.

    This may not work for Google Scholar data, depending on which subset of the record is used (may include specific search params as "citation_id" field).
    """

    for aLis1 in lis1:
        if aLis1 not in lis2:
            lis2.append(aLis1)
    return lis2


def genMasterList(authors):
    """Combine list of articles to master list."""
    masterList = []

    for k in authors.keys():
        if 'results' in authors[k].keys():
            masterList = DictListUpdate(authors[k]['results']['articles'], masterList)

    # Set to Pandas DF and use this for lazy sorting/processing (although overkill!)
    masterDF = pd.DataFrame(masterList).sort_values('year', ascending=False)
    masterDF.drop_duplicates('title', inplace=True)   # Force drop duplicate titles which may appear.

    return masterList, masterDF



#*************** FILE IO
def writeJSON(authors, fileName):
    """
    Write results to JSON

    Note that `search` objects are removed.

    """
    # Clean nested dict with Boltons, from https://stackoverflow.com/a/35280815
    bad_keys = set(['search'])

    drop_keys = lambda path, key, value: key not in bad_keys
    clean = remap(authors, visit=drop_keys)

    # Dump to file
    with open(fileName, 'w') as fp:
        json.dump(clean, fp, skipkeys=True, indent=4)

def writeHTML(masterDF, fileName = None, encoding = "utf-8", fileTime = None, authors = None):
    """
    Basic HTML file writer.

    If fileName is None no file will be written.

    """
    HTMLstr = f"""

<!doctype html>
<html>
<head>
<title>UQO Group publications (Google Scholar)</title>
<meta name="description" content="UQO Group publications">
</head>
<body>

<h1>UQO Group publications (Google Scholar)</h1>
<p class='intro'>
Group publications, automated version scraped from Google Scholar using <a href="https://serpapi.com">SerpApi</a>. See <a href="https://github.com/UQOgroup/UQO-group-publications">github repo for details</a>.
</br>
Last updated: {fileTime}</p>

"""

    # Manual formatting
    # List authors
    if authors is not None:
        HTMLstr += "<h2>Author pages</h2><ul>"
        for k,item in authors.items():
            if item['ID'] is not None:
                HTMLstr += f"<li class='author'><a href={item['URL']} <b>{k}</b></a></li>"

        HTMLstr += "</ul>"


    HTMLstr += "<h2>Publications</h2>"

    # for item in masterList:   # For vanilla list this is NOT SORTED by year
    for index, item in masterDF.iterrows():
    #     HTMLstr +=""
        HTMLstr += f"<span class='title'><a href={item['link']} <b>{item['title']}</b></a></span></br>"

        for k in ['authors','publication']:   #,'year']:
            HTMLstr += f"<span class={item[k]}>{item[k]}</br>"

        HTMLstr += "</br>"

    HTMLstr += "</body></html>"

    # With spans
    # for item in masterList[0:5]:
    #     for k in item.keys():
    #         HTMLstr += f"<span class={k}>{item[k]}</span>"

    # For IPython display:
    # from IPython.display import HTML
    # display(HTML(HTMLstr))

    # With io, see https://stackoverflow.com/a/33973211
    # Otherwise can get encoding issues here.
    # Also, can still get encoding/browser issues!
    if fileName is not None:
        with io.open(fileName,'w', encoding = encoding) as fp:
            fp.write(HTMLstr)

    return HTMLstr


#*************** Full build if called from CLI
if __name__ == "__main__":

    # Quick test settings - should pass
    # Now updated to source from ENV for GH actions
    try:
        test = os.environ['TEST']
    except:
        test = True

    testFile = 'records_2021-09-23.json'  # Set test file name, note full path appended below.


    # Set paths
    callPath = Path(sys.argv[0]).parent  # Set path as called.
    fullPath = Path(Path.cwd(), callPath)
    recordsPath = fullPath/'records'
    exportPath = Path(fullPath.parent, 'exports')

    #*** Set default file names - may also want to allow sys.argv passing here.
    apiFile = Path(fullPath, 'API_KEY.txt')
    authorsFile = Path(fullPath, 'authors.json')

    testFile = Path(recordsPath, testFile)

    # Output files
    timeString = dt.now()
    # fileTime = timeString.strftime('%Y-%m-%d_%H-%M-%S')
    fileTime = timeString.strftime('%Y-%m-%d')
    recordsFile = Path(recordsPath, f'records_{fileTime}.json')
    HTMLFile = Path(recordsPath, f'records_{fileTime}.HTML')


    # Setup
    # API_KEY = getAPIkey(apiFile)
    try:
        API_KEY = os.environ['API_KEY']
        print("Got API_KEY from env.")
    except:
        getAPIkey(apiFile)
        print("Got API_KEY from file.")


    authors = setAuthors(authorsFile)

    print("Getting Google Scholar records for...")
    print(*authors, sep = '\n')

    # Pull Google Scholar records & update
    # Note API calls may be limited, so read a file in test case.
    if not test:
        authors = getAuthors(authors)
    else:
        # For testing: read in...
        with open(testFile) as fp:
            authors = json.load(fp)

    # Process
    masterList, masterDF = genMasterList(authors)

    print("Writing output files...")
    # Write files
    writeJSON(authors, recordsFile)
    writeHTML(masterDF, fileName = HTMLFile, fileTime = fileTime, authors = authors)

    # Copy to current fileset & export formats
    currentRecords = 'UQO_group_GScholar'
    shutil.copy2(HTMLFile, Path(exportPath, currentRecords + '.html'))
    shutil.copy2(HTMLFile, Path(exportPath.parent, currentRecords + '.html'))
    shutil.copy2(HTMLFile, Path(exportPath.parent, 'docs', currentRecords + '.html'))

    print(f"Updated {HTMLFile} and {Path(exportPath.parent, currentRecords + '.html')} OK.")

    # TODO: add Pandoc converters here.
    # For a basic wrapper, try  https://stackoverflow.com/a/14028439
