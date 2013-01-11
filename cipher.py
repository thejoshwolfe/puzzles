#!/usr/bin/env python

import sys, re
import optparse
import collections, itertools
import random
import string

parser = optparse.OptionParser()
parser.add_option("-d", "--dictionary")
parser.add_option("-g", "--generate", action="store_true")
parser.add_option("-v", "--verbose", action="store_true")
options, args = parser.parse_args()

if args == ["-"]:
    args = [sys.stdin.read().strip()]

def verbose(message):
    if options.verbose:
        print(message)
verbose("reading dictionary")
dictionary = open(options.dictionary).read().split("\n")
dictionary = [word.lower() for word in dictionary if re.match("^[A-Za-z]+$", word)]

def generate_sentence(word_count):
    return [dictionary[random.randint(0, len(dictionary)-1)] for _ in range(word_count)]
def scramble(sentence):
    key = list(string.lowercase)
    random.shuffle(key)
    scrambled = ["".join(key[ord(c)-ord("a")] for c in word) for word in sentence]
    sys.stderr.write(" ".join(sentence) + "\n")
    print(" ".join(scrambled))

def solve(original_scrambled):
    original_scrambled = original_scrambled.lower()
    scrambled = re.sub("[^a-z ]", "", original_scrambled).split()
    by_signature = collections.defaultdict(list)
    verbose("building signature database")
    def get_signature(word):
        letter_index = collections.defaultdict(itertools.count().next)
        return tuple(letter_index[c] for c in word)
    for word in dictionary:
        by_signature[get_signature(word)].append(word)

    partial_keys_list = [[dict(zip(scrambled_word, real_word)) for real_word in by_signature[get_signature(scrambled_word)]] for scrambled_word in scrambled]
    # start with the ones with the fewest possibilites
    partial_keys_list.sort(key=len)
    verbose("difficulty: {0}".format(len(partial_keys_list[0])))

    def recurse(parent_key, index):
        if index == len(partial_keys_list):
            yield parent_key
            return
        for partial_key in partial_keys_list[index]:
            combined_key = dict(parent_key.items())
            def is_possible():
                for k, v in partial_key.items():
                    try:
                        if combined_key[k] != v:
                            return False
                        continue
                    except KeyError:
                        pass
                    try:
                        combined_key.values().index(v)
                        return False
                    except ValueError:
                        pass
                    combined_key[k] = v
                return True
            if not is_possible():
                continue
            for result in recurse(combined_key, index+1):
                yield result
    answer_keys = recurse({}, 0)

    answer_set = set()
    for answer_key in answer_keys:
        answer = "".join(answer_key.get(c, c) for c in original_scrambled)
        if answer not in answer_set:
            print(answer)
            answer_set.add(answer)

    sys.exit(int(not answer_set))

if options.generate:
    try:
        word_count = int(" ".join(args))
    except ValueError:
        sentence = args
    else:
        sentence = generate_sentence(word_count)
    scramble(sentence)
else:
    solve(" ".join(args))

