#! /usr/bin/python

__author__="Ramzi Abdoch <raa2148@olumbia.edu>"
__date__ ="$Feb 19, 2015"

import sys
import operator
import math

from collections import defaultdict
from count_freqs import Hmm

def usage():
    print """
    python tagger.py [counts_file] [input_file] > [output_file]
        Read in counts_file generated from training set and
        test set of data, then predict tags for each word in
        test set.

        Results are stored in the following format:

          <word> <tag> <log probability of prediction>
    """

if __name__ == "__main__":

    if len(sys.argv)!=3: # Expect exactly one argument: the training data file
        usage()
        sys.exit(2)

    try:
        counts_file = file(sys.argv[1],"r")
        test_file = file(sys.argv[2], "r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)

    # Initialize a trigram counter
    counter = Hmm(3)
    # Read in counts
    counter.read_counts(counts_file)

    # Iterate through words in test data and calculate the log probability of each tag.
    for line in test_file:
        word = line.strip()

        if word: # Nonempty line
            original_word = word
            # Check if word is absent in training set, if so, use _RARE_
            if word not in counter.all_words or counter.word_counts[word] < 5:
                word = "_RARE_"

            # Initialize dict to hold emission values
            candidates = defaultdict(float)

            # Iterate through tags
            for tag in counter.all_states:

                prob = counter.calc_emissions(word, tag)

                # Make sure not to do log(0)
                if prob == 0.0:
                    candidates[tag] = float("-inf")
                else:
                    candidates[tag] = math.log(prob)

            # Get argmax of candidates
            pred = max(candidates.iteritems(), key=operator.itemgetter(1))[0]

            # Write prediction to output file
            sys.stdout.write("%s %s %s\n" % (original_word, pred, str(candidates[pred])))
        else:
            print ""


