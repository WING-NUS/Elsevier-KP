FILE DIRECTION
====================
cache.cgi	- cacheing subsystem (runs on server), checks cached.p for keywords using DOI as key
cached.p	- serialized python hash for keywords
dict.idf.tsv	- inverse document frequency hash table, used by keyphrase.cgi
isotope.xml	- not currently used
jquery.isotope.js	- not currently used
jquery.isotope.min.js	- not currently used
js/	- not currently used
keyphrase.cgi	- CGI script on server for computing keyphrases
keyphrase.xml	- XML with caching
porter.py	- Python stemmer
porter.pyc	- (compiled) Python stemmer
query	- saved query (saved by keyphrase.cgi on call from client)
query.backup	- known good query
