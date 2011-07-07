#!/usr/bin/env python
# -*- python -*-
import cgi
import cgitb
import xml.dom.minidom
import re
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

idfDict = {}                   # inverse document frequency dictionary

freq = {}                               # freq in the document
firstPos = {}                           # first position
nthPos = {}                             # last position
ngLength = {}
inTitle = {}
score = {}

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
                if ((not re.compile("^\s*$").match(llWord)) and 
                    (not re.compile("^\s*$").match(lWord)) and
                    (not llWord.lower() in stop)):
                    insertNgram(llWord.strip() + " " + lWord.strip() + " " + w.strip(),
                                offset + wCounter,3,inTitle)
        if not (w.lower() in ngramStops or
                re.compile("^\s*$").match(w)):
            llWord = lWord
            lWord = w
        else:
            lWord = ""
            llWords = ""
        wCounter = wCounter + 1
    return offset + len(words)
    
def output(mode):
    global freq, firstPos, nthPos, ngLength, inTitle, score
    oCounter = 0;
    for k,v in sorted(score.items(), key=lambda x : x[1], reverse=True):
        if mode == "cgi":
            print "<b>", k, "</b>",
#            print ":", v, " ", freq.get(k,0), " ", firstPos.get(k,0), " ", nthPos.get(k,0), " ", \
#                  ngLength.get(k,0), " ", inTitle.get(k,0),
            print "<br/>"
            if oCounter > 10:
                return
        else:
            print k, v, freq.get(k,0), firstPos.get(k,0), nthPos.get(k,0), \
                  ngLength.get(k,0), inTitle.get(k,0)
        oCounter = oCounter + 1
    
def scoreNgrams(offset):
    global freq, firstPos, nthPos, ngLength, inTitle, idfDict, score
    for w in freq:
        if not (w in idfDict):          # assign default
            idfDict[w] = 8
        score[w] = math.log(freq[w]) * idfDict[w] * ngLength[w]
        if w in inTitle and inTitle[w] == True:
            score[w] = score[w] * 2
        first = float(firstPos[w]) / offset
        score[w] = score[w] + (10 * (1-first))
        nth = float(nthPos[w]) / offset
        score[w] = score[w] + (10 * nth)
    for w in freq:
        if ngLength[w] == 3:            # phrase, demote elements
            words = w.split(" ")
            lp = words[0] + " " + words[1]
            rp = words[1] + " " + words[2]
#            score[lp] = score.get(lp,0) / 4 * 3
#            score[rp] = score.get(rp,0) / 4 * 3
#            score[words[2]] = score.get(words[2]) / 4 * 3
#            score[w] = score[w] + score[lp]/2 + score[rp]/2 + score[words[2]]/2
        if ngLength[w] > 1:
            words = w.split(" ")
#            score[words[0]] = score.get(words[0],0) / 4 * 3
#            score[words[1]] = score.get(words[1],0) / 4 * 3
#            score[w] = score[w] + score[words[0]]/2 + score[words[1]]/2
                
def printHeader():
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers

# ---- MAIN ----
form = cgi.FieldStorage()
mode = ""
if not "query" in form:                 # invoked on command line
    mode = "cmdline"
    if len(sys.argv) != 2:
        buf = "# " + sys.argv[0] + " FATAL:\tUsage error\t" + sys.argv[0] + " <xml_filename>\n"
        sys.stderr.write(buf)
        sys.exit()
    try:
        f = open(sys.argv[1],'r') 
    except IOError:
        buf = "# " + sys.argv[0] + " FATAL:\tCan't open file with filename \"" + sys.argv[1] + "\"\n"
        sys.stderr.write(buf)
        sys.exit()
    xmlData = f.read()
    f.close()
else:                                   # invoked as CGI with query param passed
    mode = "cgi"
    xmlData = form["query"].value
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
    buf = getText(n.childNodes).encode("utf-8")
#    print n.localName, buf
    if n.localName == "h":
#        getText(n.childNodes).encode("utf-8")
        hCounter = hCounter+1
    elif n.localName == "title":
        flags = {"title":1}
        buf = getText(n.childNodes).encode("utf-8")
        offset = compileNgrams(buf,offset,flags)
        tCounter = tCounter+1
    elif n.localName == "p":
        flags = {}
        buf = getText(n.childNodes).encode("utf-8")
#        print buf
        offset = compileNgrams(buf,offset,flags)
        pCounter = pCounter+1
loadDict("dict.idf.tsv")
scoreNgrams(offset)
output(mode)
