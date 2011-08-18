#!/usr/bin/env python
# -*- python -*-
import cgi
import cgitb
import xml.dom.minidom
import cPickle as pickle
import os
import re
import sys
import math
# import svm
from porter import *

# cgitb.enable()
stop = ["the","a","an",
        "of","in","out","above","below","at","by","to","for","on","with","into","onto","upto","from","to",
        "is","was","be","are","have","has","been",
        "can","could","would","should","might","shall","will",
        "this","that","these","those",
        "i","you","me","mine","he","his","she","her","hers","they","theirs","we","their","our","ours","it","its",
        "and","but","or","then","because","so","if","else","however","as","although","whereas","thus",
        "who","whom","where","when","why","how","which","what",
        "no","non","not",
        ]
ngramStops = ["the","a","an",
              "is","was","be","are","have","has","been",
              "can","could","would","should","might","shall","will",
              "this","that","these","those",
              "i","you","me","mine","he","his","she","her","hers","they","theirs","we","their","our","ours","it","its",
              "who","whom","where","when","why","how","which","what",
              ]

# globals
## configurables
numKeywords = 15
idfDictionaryName = "dict.idf.tsv"
cpickledCacheName = "cached.p"

idfDict = {}                   # inverse document frequency dictionary

freq = {}                               # freq in the document
firstPos = {}                           # first position
nthPos = {}                             # last position
ngLength = {}
inTitle = {}
subsumed = {}                           
subsumedRatio = {}
score = {}
# end globals

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def insertNgram(w,offset,len,presentInTitle):
    global freq, firstPos, nthPos, ngLength, inTitle, score
    freq[w] = freq.get(w,0) + 1
    if w in firstPos:
        pass
    else:
        firstPos[w] = offset
    nthPos[w] = offset
    ngLength[w] = len
    if w in inTitle and inTitle[w] == True:
        pass
    else:
        inTitle[w] = presentInTitle

def loadDict(file):
    global idfDict
    try:
        f = open(file,'r')
    except IOError:
        buf = "# " + sys.argv[0] + " FATAL:\tCan't open file with filename \"" + sys.argv[1] + "\"\n"
        sys.stderr.write(buf)
        sys.exit()
    for line in f:
        (w,idf) = line.split("\t")
        idfDict["w"] = float(idf)
    
def compileNgrams(s,offset,flags):
    global subsumed
    words = re.compile("[^\w]+").split(s)
    lWord = llWord = ws = ""
    wCounter = 0
    inTitle = False
    if "title" in flags and flags["title"] == 1:
        inTitle = True
    for w in words:
        if not (re.compile("^\s*$").match(w) or # skip blank words
                w.lower() in stop or    # skip stop words
                len(w) == 1):           # skip one letter words
            # ws = stemmer.stem(w,0,len(w)-1).lower()
            ws = w
            insertNgram(ws,offset + wCounter,1,inTitle)
            if not (w.lower() in ngramStops):
                if ((not re.compile("^\s*$").match(lWord)) and 
                    (not lWord.lower() in stop)):
                    insertNgram(lWord.strip() + " " + w.strip(), offset + wCounter,2,inTitle)
#                    print ws + ": " + lWord.strip() + " " + w.strip(),
                    subsumed[ws] = subsumed.get(ws,0) + 1 # calculate subsumption
#                    print subsumed[ws]
                if ((not re.compile("^\s*$").match(llWord)) and 
                    (not re.compile("^\s*$").match(lWord)) and
                    (not llWord.lower() in stop)):
                    insertNgram(llWord.strip() + " " + lWord.strip() + " " + w.strip(),
                                offset + wCounter,3,inTitle)
                    subsumed[lWord.strip() + " " + ws] = subsumed.get(lWord.strip() + " " + ws,0) + 1
        if not (w.lower() in ngramStops or
                re.compile("^\s*$").match(w)):
            llWord = lWord
            lWord = w
        else:
            lWord = ""
            llWords = ""
        wCounter = wCounter + 1
    return offset + len(words)
    
def output(mode,doi):
    global freq, firstPos, nthPos, ngLength, inTitle, score, subsumed, subsumedRatio, numKeywords
    cache = {}
    try: 
        cacheFH = open(cpickledCacheName)
        cache = pickle.load(cacheFH)
        cacheFH.close()
    except IOError:
        pass                            # no-op
    oCounter = 0;
    keywordList = []
    for k,v in sorted(score.items(), key=lambda x : x[1], reverse=True):
        keywordList.append(k)
        if mode == "cgi":
            # BUG: probably should check for other
            # things aside from just spaces
#            escapedQueryTerms = k.replace(" ","+")
#            print "<span class=\"ex1\">",
#            print "<a href=\"javascript:void(0);\" onclick=\"gadgets.ScienceDirect.executeSearch('",
#            print "\"",
#            print escapedQueryTerms,
#            print "\"",
#            print "');\">",
            sys.stdout.write(k)
            sys.stdout.write(",")
#            print "</a>",
#            print "</span>",
#            print ":", v, " ", freq.get(k,0), " ", firstPos.get(k,0), " ", nthPos.get(k,0), " ", \
#                  ngLength.get(k,0), " ", inTitle.get(k,0),
#            print "<br/>"
            if oCounter > numKeywords:
                break
        else:
            print k, v, freq.get(k,0), firstPos.get(k,0), nthPos.get(k,0), \
                  ngLength.get(k,0), inTitle.get(k,0), subsumed.get(k,0), subsumedRatio.get(k,0)
        oCounter = oCounter + 1
        cache[doi] = keywordList
    # try to pickle the data
    try: 
        cacheFH2 = open(cpickledCacheName,'wb')
        pickle.dump(cache,cacheFH2)
        cacheFH2.close()
        try:
            os.chmod(cpickledCacheName,0777)
        except:
            pass                        # may have permission problems
    except:
        print "Unexpected error:", sys.exc_info()[0]
    
def scoreNgrams(offset):
    global freq, firstPos, nthPos, ngLength, inTitle, idfDict, score, subsumed, subsumedRatio
    for w in freq:
        if not (w in idfDict):          # assign default
            idfDict[w] = 8
        subsumedRatio[w] = 1.0 * subsumed.get(w,0) / freq[w]
        score[w] = math.log(freq[w]) * idfDict[w] * ngLength[w] * (1 - subsumedRatio[w])
        if w in inTitle and inTitle[w] == True:
            score[w] = score[w] * 2
        first = float(firstPos[w]) / offset
        score[w] = score[w] + (10 * (1-first))
        nth = float(nthPos[w]) / offset
        score[w] = score[w] + (10 * nth)
                
def printHeader():
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers

# ---- MAIN ----
form = cgi.FieldStorage()
mode = ""
doi = ""
if not "query" in form:                 # invoked on command line
#    mode = "cmdline"
    mode = "cgi"
    if len(sys.argv) != 3:
        buf = "# " + sys.argv[0] + " FATAL:\tUsage error\t" + sys.argv[0] + " <xml_filename> <doi>\n"
        sys.stderr.write(buf)
        sys.exit()
    try:
        f = open(sys.argv[1],'r') 
    except IOError:
        buf = "# " + sys.argv[0] + " FATAL:\tCan't open file with filename \"" + sys.argv[1] + "\"\n"
        sys.stderr.write(buf)
        sys.exit()
    xmlData = f.read()
    doi = sys.argv[2]
    f.close()
else:                                   # invoked as CGI with query param passed
    mode = "cgi"
    xmlData = form["query"].value
    doi = form["doi"].value
    f = open('query','w')
    f.write(xmlData)
    f.close()
    printHeader()
    
xmlData = removeNonAscii(xmlData);
doc = xml.dom.minidom.parseString(xmlData)

# initialize porter stemmer
stemmer = PorterStemmer()
nodes = doc.getElementsByTagName("*")

offset = 0
counter = hCounter = tCounter = pCounter = 1
for n in nodes:
    counter = counter+1
    buf = getText(n.childNodes).encode("utf-8") # go through all text nodes
#    print n.localName, buf
    if n.localName == "h":              # header
#        getText(n.childNodes).encode("utf-8")
        hCounter = hCounter+1
    elif n.localName == "title":        # title
        flags = {"title":1}
        buf = getText(n.childNodes).encode("utf-8")
        offset = compileNgrams(buf,offset,flags)
        tCounter = tCounter+1
    elif n.localName == "p":            # normal paragraph
        flags = {}
        buf = getText(n.childNodes).encode("utf-8")
#        print buf
        offset = compileNgrams(buf,offset,flags)
        pCounter = pCounter+1
loadDict(idfDictionaryName)
scoreNgrams(offset)
output(mode,doi)
