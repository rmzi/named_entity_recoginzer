#! /usr/bin/python

__author__="Ramzi Abdoch <raa2148@olumbia.edu>"
__date__ ="$Feb 19, 2015"

import sys
from collections import defaultdict

import fileinput
from count_freqs import Hmm

import math

def usage():
    print """
    python replace_rare.py [counts_file] [input_file]
        Read in named entity tagged training input file
        and corresponding counts_file and replace words
        satisfying count(word) < 5 with common symbol _RARE_.
    """

# Original code written by Jason (http://stackoverflow.com/users/26860/jason), but modified
# Code in this thread: http://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
def replaceAll(file,candidates,replaceExp):
    for line in fileinput.input(file, inplace=True):
            parts = line.strip().split(" ")

            # If the word in the line is a word where count(word) < 5
            if parts[0] in candidates:
                # Replace with _RARE_
                parts[0] = replaceExp
                line = " ".join(parts) + "\n"
            sys.stdout.write(line)

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

    print "# of words where count(word) < 5", len(low_words)
    print "# of words where count(word) > 5", len(high_words)

    # Replace each instance of word in low_words with _RARE_ in training set
    replaceAll(output, low_words, '_RARE_')