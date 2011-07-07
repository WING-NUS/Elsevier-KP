#!/usr/bin/env python
# -*- python -*-
from svmutil import * # make sure that libsvm.so.2 is in parente directory
from porter import *
from xml.dom.minidom import parse
import re

stop = ["the","a","an",
        "of","in","out","above","below","at","by","to","for","on","with","into","onto","upto",
        "is","was","be","are","have","has","been",
        "can","could","would","should","might","shall","will",
        "this","that","these","those",
        "i","you","me","mine","he","his","she","her","hers","they","theirs","we","their","our","ours","it","its",
        "and","but","or","then","because","so","if","else","however","as","although","whereas","thus",
        "who","whom","where","when","why","how","which","what",
        "no","non","not",
        ]

freq = {}                                       # freq in the document
first_pos = {}                                        # first position
nth_pos = {}                                           # last position

def compile_ngrams(s,offset):
  global freq, first_pos, nth_pos
  output = ""
  words = re.compile("[^\w]+").split(s)
  for w in words:
    if re.compile("^\s*$").match(w): continue       # skip blank words
    if w.lower() in stop: continue
    if len(w) == 1: continue
    output += stemmer.stem(w,0,len(w)-1).lower() + " "
    freq[w] = 1 if w not in freq else freq[w] + 1
    if w not in first_pos: first_pos[w] = offset
    nth_pos[w] = offset

  return offset + len(words)

def output():
  global freq
  for k,v in sorted(freq.items(), key=lambda x : x[1]):
    print k, v, first_pos[k], nth_pos[k]

doc = parse(sys.argv[1])                   # parse an XML file by name

for kw in doc.getElementsByTagName('ce:keyword'):
  for tn in kw.getElementsByTagName('ce:text'):
    print tn.firstChild.data

for title in doc.getElementsByTagName('ce:title'):
  print "TITLE ", title.firstChild.data
  break                                                             # only run once

for st in doc.getElementsByTagName('ce:section-title'):
  print "SECTION ", st.firstChild.data

stemmer = PorterStemmer()
offset = 0
for p in doc.getElementsByTagName('ce:para'):
  buf = p.firstChild.data
  offset = compile_ngrams(buf,offset)
  print offset
  print " "

output()
