#!/usr/bin/env python

import sys, re
import optparse
import collections, itertools
import random
import string
import math

parser = optparse.OptionParser()
parser.add_option("-d", "--dictionary")
parser.add_option("-g", "--generate", action="store_true")
parser.add_option("-v", "--verbose", action="store_true")
options, args = parser.parse_args()

if args == ["-"]:
    args = [sys.stdin.read().strip()]

last_progress_line = ""
def clear_progress():
    if not options.verbose: return
    sys.stdout.write("\r")
def restore_progress():
    sys.stdout.write(last_progress_line)
    sys.stdout.flush()
def show_progress(out_of_1):
    if not options.verbose: return
    line = "{0:.1f}%".format(out_of_1*100)
    global last_progress_line
    if line == last_progress_line: return
    clear_progress()
    sys.stdout.write(line)
    sys.stdout.flush()
    last_progress_line = line
def say(message):
    clear_progress()
    message += " " * (len(last_progress_line) - len(message))
    print(message)
    restore_progress()

dictionary = open(options.dictionary).read().split("\n")
dictionary = [word.lower() for word in dictionary if re.match("^[A-Za-z]+$", word)]

def generate_sentence(word_count):
    sentence = " ".join(dictionary[random.randint(0, len(dictionary)-1)] for _ in range(word_count))
    sentence += "."
    if options.verbose:
        sys.stderr.write(sentence + "\n")
    return sentence
def scramble(sentence):
    words = split(sentence)
    order = list(string.lowercase)
    random.shuffle(order)
    key = dict(zip(string.lowercase, order))
    scrambled = "".join(key.get(c, c) for c in sentence)
    print(scrambled)

def split(sentence):
    return re.sub("[^a-z ]", "", sentence).split()

def count_combinations(n, r):
    f = math.factorial
    return f(n)/(f(r)*f(n-r))

def solve(original_scrambled):
    original_scrambled = original_scrambled.lower()
    scrambled = split(original_scrambled)
    by_signature = collections.defaultdict(list)
    def get_signature(word):
        letter_index = collections.defaultdict(itertools.count().next)
        return tuple(letter_index[c] for c in word)
    for word in dictionary:
        by_signature[get_signature(word)].append(word)

    # starting with words with the most letters results in smoother progress
    if options.verbose:
        scrambled.sort(key=lambda word: -max(get_signature(word)))
    partial_keys_list = [[dict(zip(scrambled_word, real_word)) for real_word in by_signature[get_signature(scrambled_word)]] for scrambled_word in scrambled]
    # starting with words with the fewest possibilites results in fastest solve time
    if not options.verbose:
        partial_keys_list.sort(key=len)
    # this is the test case used to measure performance:
    # "the time has come the walrus said to talk of many things.  of shores and ships and sealing wax, of cabbages and kings.  carroll"

    # eliminate any impossible words
    partial_keys_list = [partial_keys for partial_keys in partial_keys_list if len(partial_keys) != 0]
    # this test case has immediately impossible words:
    # "when on a music staff, ff for fortissimo means very loud, much like mournful howls voiced by frustrated solvers."

    def recurse(parent_key, index, significance):
        if index in compromized_indexes:
            # pass through
            for result in recurse(parent_key, index+1, significance):
                yield result
            return
        if index == len(partial_keys_list):
            yield parent_key
            return
        progress_step = significance / len(partial_keys_list[index])
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
                show_progress(progress[0])
                progress[0] += progress_step
                continue
            for result in recurse(combined_key, index+1, progress_step):
                yield result
    def announce_compromizes(compromizes):
        if not options.verbose: return
        if compromizes == 0: return
        say("leaving out {0} word{1}.".format(compromizes, "s"[0:bool(compromizes - 1)]))
    answer_set = set()
    for omission_count in range(len(partial_keys_list)):
        announce_compromizes(len(scrambled) - len(partial_keys_list) + omission_count)
        combination_count = count_combinations(len(partial_keys_list), omission_count)
        progress = [0]
        # try leaving out random words (starting by including them all)
        for omissions in itertools.combinations(range(len(partial_keys_list)), omission_count):
            compromized_indexes = set(omissions)
            significance = 1.0/combination_count
            answer_keys = recurse({}, 0, significance)

            for answer_key in answer_keys:
                answer = "".join(answer_key.get(c, c) for c in original_scrambled)
                if answer not in answer_set:
                    say(answer)
                    answer_set.add(answer)

        if answer_set:
            clear_progress()
            break

if options.generate:
    sentence = " ".join(args)
    try: word_count = int(sentence)
    except ValueError: pass
    else: sentence = generate_sentence(word_count)
    scramble(sentence)
else:
    solve(" ".join(args))

