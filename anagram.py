#!/usr/bin/env python

import optparse
import collections
import sys

parser = optparse.OptionParser()
parser.add_option("-d", "--dictionary")
parser.add_option("-q", "--quiet", action="store_true")
options, args = parser.parse_args()
if sys.stderr.isatty() and not sys.stdout.isatty():
    # don't leave stderr alone
    options.quiet = True

def warn(message):
    if not options.quiet:
        sys.stderr.write(message)

warn("initializing dictionary...")
dictionary = open(options.dictionary).read().split("\n")
anagrams = collections.defaultdict(list)
key_for = lambda word: str(sorted(word))
for word in dictionary:
    anagrams[key_for(word)].append(word)
warn("done\n")

for arg in args:
    warn("{0} -> ".format(arg))
    print(" ".join(anagrams[key_for(arg)]))
