#! /usr/bin/python

__author__="Ramzi Abdoch <raa2148@olumbia.edu>"
__date__ ="$Feb 19, 2015"

import sys
import math
import string
import fileinput

from collections import defaultdict
from count_freqs import Hmm

def usage():
    print """
    python group_rare.py [counts_file] [input_file]
        Read in named entity tagged training input file
        and corresponding counts_file and group words
        based on defined criteria. Replace all grouped
        words in the training symbol for a common symbol
        for said group in the form _GROUPID_.
    """

# Original code written by Jason (http://stackoverflow.com/users/26860/jason), but modified
# Code in this thread: http://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
def replace_all(file,candidates,replaceExp):
    for line in fileinput.input(file, inplace=True):
            parts = line.strip().split(" ")

            # If the word in the line is a word where count(word) < 5
            if parts[0] in candidates:
                # Replace with replaceExp
                parts[0] = replaceExp
                line = " ".join(parts) + "\n"
            sys.stdout.write(line)

# Helper functions, for cleanliness
def cap_first(word):
    return word.istitle()

def all_caps(word):
    return word.isupper()

def num_punct(word):
    return all(c in string.punctuation or c.isdigit() for c in word)

def filter_out(idxs, source):
    for key in idxs:
        source.pop(key, None)

if __name__ == "__main__":

    if len(sys.argv)!=3: # Expect exactly two arguments: the counts and corresponding training data file
        usage()
        sys.exit(2)

    try:
        input = file(sys.argv[1],"r")
        output = sys.argv[2]
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)

    # Initialize a trigram counter
    counter = Hmm(3)
    # Read in counts
    counter.read_counts(input)

    # Filter words with count < 5
    low_words = dict((k,v) for k, v in counter.word_counts.iteritems() if v < 5)
    high_words = dict((k,v) for k,v in counter.word_counts.iteritems() if v > 5)

    # Filter words starting with a capital letter.
    cf = dict((k,v) for k, v in low_words.iteritems() if cap_first(k))

    # Filter words with only numbers and punctuation/dashes
    np = dict((k,v) for k,v in low_words.iteritems() if num_punct(k))

    # Filter words with all caps
    ac = dict((k,v) for k, v in low_words.iteritems() if all_caps(k))

    # Remove all filtered values from low_words
    filter_out(cf, low_words)
    filter_out(np, low_words)
    filter_out(ac, low_words)

    # Replace each instance of word in buckets with respective _GROUPID_
    replace_all(output, low_words, '_RARE_')
    replace_all(output, cf, '_CF_')
    replace_all(output, np, '_NP_')
    replace_all(output, ac, '_AC_')
