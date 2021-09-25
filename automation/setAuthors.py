"""
Basic script to set authors > human readable JSON file.
"""

# Set author list
# Note Phil & Andy currently missing from Google Scholar Profiles.

authorList = { 'Ben Sussman':{'ID':'IDU7HMMAAAAJ'},
            'Rune Lausten':{'ID':'Sx-Dx4cAAAAJ'},
            'Paul Hockett':{'ID':'e4FgTYMAAAAJ'},
            'Duncan England':{'ID':'IzqvkioAAAAJ'},
            'Phil Bustard':{'ID':None},
            'Andrew Ridsdale':{'ID':None},
            'Khabat Heshami':{'ID':'fBBMAKwAAAAJ'},
          }

# Dump to file - OK
import json
with open('authors.json', 'w') as fp:
    json.dump(authorList, fp, indent=4, sort_keys=True)
