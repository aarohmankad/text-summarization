#!/usr/bin/python3
# This script will calculate the document frequency of all words
# in all the articles.

# We are pre-computing these values for use later to see which
# sentences are "useful" in a summary

import glob
import string
from nltk import word_tokenize
from nltk.corpus import stopwords

# Get all story filenames
# DEVELOPMENT: a subset of all stories
# files = glob.glob("/home/aaroh/Documents/cs173/hw5/cnn/stories/fa*");
# PRODUCTION: all stories
files = glob.glob("/home/aaroh/Documents/cs173/hw5/cnn/stories/*");

N = len(files)
stop_words = stopwords.words('english')
translator = str.maketrans('', '', string.punctuation)

df = {}

i = 1
for filename in files:
  file = open(filename, 'r').read()

  raw_words = file.translate(translator)

  tokens = [word.lower() for word in word_tokenize(raw_words) if word not in stop_words]
  for token in tokens:
    if token in df:
      df[token].add(filename)
    else:
      df[token] = set([filename])

  print('{i}: {filename}'.format(i=i, filename=filename))
  i = i+1

file = open('df', 'w+')
for word in df:
  doc_freq = len(df[word])
  file.write("{word}\t{doc_freq}\n".format(word=word, doc_freq=doc_freq))

file.close()
