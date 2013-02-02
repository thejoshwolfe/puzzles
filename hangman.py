#!/usr/bin/env python

import sys
import re
import random

import optparse
parser = optparse.OptionParser()
parser.add_option("-d", "--dictionary")
parser.add_option("-m", "--min-word-length", type=int, default=8)
parser.add_option("-n", "--word-count", type=int, default=1)
parser.add_option("-l", "--lives", type=int, default=8)

options, args = parser.parse_args()

dictionary_path = options.dictionary or "/etc/dictionaries-common/words"
try:
    dictionary = re.findall("^[a-z]+$", open(dictionary_path).read(), re.MULTILINE)
except IOError:
    if options.dictionary == None:
        sys.exit("ERROR: missing -d")
    raise

def generate():
    words = [word for word in dictionary if len(word) >= options.min_word_length]
    return [words[random.randint(0, len(words)-1)] for _ in range(options.word_count)]

def host(answer):
    reveals = {c: "_" for word in answer for c in word}
    mistakes = set()
    max_health = options.lives
    while True:
        print("")
        status = "   ".join(" ".join(reveals[c] for c in word) for word in answer)
        status += "    "
        status += "[{}]".format("".join(sorted(mistakes)).ljust(max_health))
        print(status)
        if "_" not in reveals.values():
            print("winner")
            return
        if len(mistakes) >= max_health:
            break
        try:
            guess = raw_input("> ")[:1]
        except EOFError:
            print("")
            break
        if not guess: break
        if not re.match("[a-z]", guess): continue
        try:
            reveals[guess]
            reveals[guess] = guess
        except KeyError:
            mistakes.add(guess)
    print("loser")
    return " ".join(answer)

if len(args) == 0:
    sys.exit(host(generate()))

