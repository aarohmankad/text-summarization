#!/usr/bin/python3

import fileinput
import glob
import math
import sys
import string
from collections import Counter
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

filename = sys.argv[1]
files = glob.glob("/home/aaroh/Documents/cs173/hw5/cnn/stories/*");
N = len(files)
stop_words = stopwords.words('english')
translator = str.maketrans('', '', string.punctuation)
df = fileinput.input('df')

# Calculate Term Frequencies
tf = {}

file = open(filename, 'r').read()
raw_words = file.translate(translator)

tokens = [word.lower() for word in word_tokenize(raw_words) if word not in stop_words]
for token in tokens:
  if token in tf:
    tf[token] += 1
  else:
    tf[token] = 1

# Calculate Inverse Document Frequencies
idf = {}
for line in df:
  (term, freq) = line.strip().split('\t')
  idf[term] = math.log(N / int(freq))

# Calculate TFIDF Weights
tfidf = {}
for token in tf:
  tfidf[token] = tf[token] * idf[token]

sentences = sent_tokenize(file)
weighted_sentences = {}

for s in sentences:
  weight = 0;

  for word in word_tokenize(s):
    if word in tfidf:
      weight += tfidf[word]
      
  weighted_sentences[s] = weight

sorted_weights = Counter(weighted_sentences)
summary = sorted_weights.most_common(5)
ordered_summary = {}

for (s, weight) in summary:
  ordered_summary[sentences.index(s)] = s

for order in sorted(ordered_summary.keys()):
  # Optionally remove highlights, which are essentially ads
  if "@highlight" in ordered_summary[order]:
    continue
  print(f"{ordered_summary[order]}\n")
