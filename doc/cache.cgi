#!/usr/bin/env python
# -*- python -*-
import cgi
import cgitb
import cPickle as pickle
import os
import re
import sys
# import svm
from porter import *

# globals
## configurables
cpickledCacheName = "cached.p"

# end globals

def printHeader():
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers

def output(mode,doi):
    global cache
    keywordList = cache.get(doi,0)
    for k in keywordList:
        if mode == "cgi":
            # BUG: probably should check for other
            # things aside from just spaces
#            escapedQueryTerms = k.replace(" ","+")
#            print "<span class=\"ex1\">",
#            print "<a href=\"javascript:void(0);\" onclick=\"gadgets.ScienceDirect.executeSearch('",
#            print escapedQueryTerms,
#            print "');\">",
            print k, ",",
#            print "</a>",
#            print "</span>",
#            print ":", v, " ", freq.get(k,0), " ", firstPos.get(k,0), " ", nthPos.get(k,0), " ", \
#                  ngLength.get(k,0), " ", inTitle.get(k,0),
#            print "<br/>"
        else:
            print k

# ---- MAIN ----
# load cache
cache = {}
try: 
    cacheFH = open(cpickledCacheName)
    cache = pickle.load(cacheFH)
    cacheFH.close()
except IOError:
    pass                            # no-op

form = cgi.FieldStorage()
mode = ""
doi = ""
if not "doi" in form:                 # invoked on command line
#    mode = "cmdline"
    mode = "cgi"
    if len(sys.argv) != 2:
        buf = "# " + sys.argv[0] + " FATAL:\tUsage error\t" + sys.argv[0] + " <doi>\n"
        sys.stderr.write(buf)
        sys.exit()
    doi = sys.argv[1]
else:                                   # invoked as CGI with query param passed
    mode = "cgi"
    doi = form["doi"].value
    printHeader()

if cache.get(doi,0) == 0:
    print "0"
else:
   output(mode,doi)
