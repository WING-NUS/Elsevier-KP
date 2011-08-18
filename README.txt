FILE DIRECTORY

Currently all files live in the doc/ subdirectory until the rest of
the backend system gets built up by Min.

====================
doc/cache.cgi	- cacheing subsystem (runs on server), checks cached.p for keywords using DOI as key
doc/cached.p	- serialized python hash for keywords
doc/dict.idf.tsv	- inverse document frequency hash table, used by keyphrase.cgi
doc/isotope.xml	- not currently used
doc/jquery.isotope.js	- not currently used
doc/jquery.isotope.min.js	- not currently used
doc/js/	- not currently used
doc/keyphrase.cgi	- CGI script on server for computing keyphrases (Jud working on this).
doc/keyphrase.xml	- XML with caching
doc/porter.py	- Python stemmer
doc/porter.pyc	- (compiled) Python stemmer
doc/query	- saved query (saved by keyphrase.cgi on call from client)
doc/query.backup	- known good query
