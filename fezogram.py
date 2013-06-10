#!/usr/bin/env python

"""i would say 'spoiler alert', except that this doesn't succeed at solving any puzzles :/"""

import optparse
import re

parser = optparse.OptionParser()
parser.add_option("-d", "--dictionary")
parser.add_option("-l", "--min-word-length", type=int)
parser.add_option("-s", "--min-sub-length", type=int)
parser.add_option("-i", "--case-insensitive", action="store_true", default=False)
parser.add_option("-x", "--exclude-word", action="append")
options, args = parser.parse_args()

def maybe_lower_list(words):
  if options.case_insensitive:
    words = [word.lower() for word in words]
  return words

letter_groups = [set(letters) for letters in maybe_lower_list(args)]
exclude_words = set(options.exclude_word or [])

min_length = options.min_word_length
min_sub_length = options.min_sub_length
dictionary = [word for word in maybe_lower_list(open(options.dictionary).read().split("\n")) if word not in exclude_words]
dictionary_set = set(dictionary)

# find compound words
for word in dictionary:
  # length check
  if min_length != None and len(word) < min_length:
    continue
  # compound word check
  compound_word_note = ""
  if min_sub_length != None:
    splits = ((word[:i], word[i:]) for i in range(min_sub_length, len(word)+1-min_sub_length))
    good_splits = [(a, b) for (a, b) in splits if a in dictionary_set and b in dictionary_set]
    if len(good_splits) == 0:
      continue
    justify = " " + " " * (len(letter_groups) - len(word))
    compound_word_note = "".join(justify + " ".join(split) for split in good_splits)
  # letter groups check
  if len(letter_groups) != 0:
    groups = letter_groups[:]
    def remove_group(c):
      for g in groups:
        if c in g:
          groups.remove(g)
          return True
    if not all(remove_group(letter) for letter in word):
      continue
  print(word + compound_word_note)

