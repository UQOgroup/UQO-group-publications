# UQO group publications list

Ultrafast Quantum Optics (UQO) group publications lists

TLDR: for an [up-to-date publications list see the Google Scholar scrape here](https://uqogroup.github.io/UQO-group-publications/UQO_group_GScholar.html).

Two versions...

## (1) Ongoing group curated version

The main `group_ongoing.bib` file is manually updated, and rendered via [BibBase](https://bibbase.org/) on [the group website](http://femtolab.ca/wordpress/?p=242); see also [quantumtechnology.ca](http://quantumtechnology.ca/publications) for a current QT list.

### To view

* Bibase-rendered interactive version on [the group website](http://femtolab.ca/wordpress/?p=242)
* Download the .bib and use your favourite tools (e.g. JabRef, Zotero...).

### To edit

A few options:

1. **Easiest**: Sign in to Github with your UQOgroup credentials, then edit `group_ongoing.bib` directly [in the web interface (pencil icon at top right of the document)](https://github.com/UQOgroup/UQO-group-publications/blob/main/group_ongoing.bib).
2. Fork the repo to your own Github account, and make changes there - the web interface will also do this this if you are not signed in to the group account (you'll get a message that you can't edit directly).
3. Pull to a local copy and edit this.

In the latter cases, to update the main repo you'll either need to sign in as a group member, or send a pull request from your own Github account (this should, probably, auto-merge). To permanently allow editing from your own Github account, sign in as a group member then add your other account via Settings > Manage Access.

## (2) Automated list from Google Scholar

Scraped from Google Scholar pages [via SerpAPI](https://serpapi.com/). This is updated weekly (via a Github action). Note there is less information here than in the full Bibtex files (due to API limitations), although all items link to the relevant Google Scholar page for more details & additional article links.

- [Rendered output via Github pages](https://uqogroup.github.io/UQO-group-publications/UQO_group_GScholar.html).
- [Rendered output on the group website](http://femtolab.ca/?p=1321).
- Various formats in `/exports` (TODO)
- Source code in `/automation`
- Action in `/.github/actions`

SerpAPI details:

- [Guide](https://serpapi.com/google-scholar-author-api)
- [Playground](https://serpapi.com/playground?engine=google_scholar_author)
- [Pypi](https://pypi.org/project/google-search-results/)
