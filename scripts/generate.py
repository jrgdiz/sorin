#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random
import json
import xml.sax.saxutils
import random

with open("archive/"+sys.argv[1]+"/json", 'r') as f:
  chain = json.load(f)

with open("archive/"+sys.argv[1]+"/json2", 'r') as f:
  chain2 = json.load(f)

with open("archive/"+sys.argv[1]+"/log", 'r') as f:
  tweets = [l.strip() for l in f.readlines()]

####
# jump back a random distance
def backjump():
  global sentence, numchars, curr, prev
  cutpoint = random.randint(1, len(sentence))
  for i in range(1, cutpoint):
    popped = sentence.pop()
    numchars = numchars - 1 - len(popped)
  try:
    prev = sentence[-2]
  except IndexError:
    prev = "\n"
  try:
    curr = sentence[-1]
  except IndexError:
    curr = "\n"
####

output = tweets[0] # hack to guarantee a first iteration
while output in tweets:

  prev = "\n"
  curr = "\n"
  numchars = -1 # offset the extra space counted in the first word
  sentence = []
  while True:
    if random.choice([True, False]):
      choices = [x for x in chain[curr]]
    else:
      choices = [x for x in chain2[prev+" "+curr]]
    if [] == choices:
      backjump()
      continue
    word = random.choice(choices)
    if not word:
      break # end of sentence
    else:
      if (numchars + 1 + len(word)) >= 140:
        backjump()
        continue
      else:
        numchars += 1 + len(word)
        sentence.append(word)
        prev = curr
        curr = word
  output = " ".join(sentence)

# we leave ! and ? since they make sense isolated
output = [w.translate(str.maketrans('', '', '"()[]{}«»¡¿')) for w in output.split()]
output = " ".join(output)

print(xml.sax.saxutils.unescape(output))