# -*- coding: utf-8 -*-

# General Requirements
import csv
import requests
import pandas
import caffeine
import os
import json
from bs4 import BeautifulSoup
import re
from collections import Counter
from nltk import sent_tokenize

# compile JSONs from HTML/JS queries
root = "/PATH/" # Your path here
filenames=[]
for path, subdirs, files in os.walk(root):
  for name in files:
    if ".DS_Store" not in name:
      filenames.append(os.path.join(path, name))

all_results = pandas.DataFrame() 

for f in filenames:
  these_results = json.load(open(f))
  try:
    q = these_results["queries"]["request"][0]["exactTerms"] 
    print(q)
  except KeyError:
    q = these_results["queries"]["request"][0]["searchTerms"] 
    print(q)
  try:
    these_results = pandas.DataFrame(these_results["items"])
    these_results["query"] = q
    all_results = pandas.concat([all_results, these_results])
  except KeyError:
    print("no items")
  
# Drop any duplicates - some search queries may have found the same page. We'll remove whichever one comes first in the table.
pages = all_results.drop_duplicates(subset='link', keep="first") # keep first link which should be most recent - this is most conservative approach in terms of timeline
pages.reset_index(inplace=True)
pages = pages[['link','title', 'snippet']] # drop unnecessary columns

# Set up columns for collecting phrases in an deductive analysis
terms = ['AI',
 'artificial intelligence',
 'data',
 'algorithms'
]
grammar = [
    'is',
    'is not',
    "isn't",
    'will',
    'will not',
    "won't",
    'could',
    'could not',
    "couldn't",
    'can',
    'cannot',
    "can't",
    'are',
    'are not',
    "aren't"
    ]
for word in grammar:
  pages[word] = None
  
# Visit pages, scrape, and count terms
for index, page in pages.iterrows():
  print(index)
  
  # Back up results every 50 links...
  if index % 50 == 0:
    pages.to_csv("googledump"+str(index)+".csv")
    print("exported")
  
  link=page["link"]
  
  try:
    # Visit the page
    response = requests.get(link, timeout=120) # Give it up to 2 minutes to get the link

    try:
      content = response.content.decode()
      content = BeautifulSoup(content, 'html.parser') # Beautiful Soup the content....pull out key HTML structures
      x = [s.extract() for s in content(['style', 'script', '[document]', 'head', 'title'])] # This is most important to do here to get an accurate _inductive_ count. Probably doesn't matter when we go _looking_ for particular terms, except maybe with "data"
      del x # removing unnecessary parts of the page - the style, script, document, head, and title elements
      body = content.get_text() # Get the text  
      sentences=sent_tokenize(body) # Form sentences out of the text
      
      # Count phrases e.g. artificial intelligence is...isn't....won't....etc.
      for term in terms:
        for word in grammar:
          phrase = term + " " + word
          phrases = []
          for sentence in sentences: 
            if phrase in sentence:
              phrases.append(sentence)
              #print(phrases) # Debugging
          if len(phrases) > 0:
            pages.iloc[index,[pages.columns.get_loc(word)]] = phrases  # Accounting for zero indexing
      
    except:
      print("Can't get phrases")
      
  except:
    print("Unable to look up page")

pages.to_csv("googlephrases.csv")