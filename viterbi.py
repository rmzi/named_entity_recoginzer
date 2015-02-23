#! /usr/bin/python

__author__="Ramzi Abdoch <raa2148@olumbia.edu>"
__date__ ="$Feb 19, 2015"

import sys
import operator
import math

from collections import defaultdict
from count_freqs import Hmm

def word_iterator(corpus_file):
    """
    Modification of corpus iterator in count_freqs.py w/o tags
    Return words in corpus_file
    """
    l = corpus_file.readline()
    while l:
        line = l.strip()
        if line:
            yield line
        else
            yield None
        l = corpus_file.readline()

def sent_iterator(word_iterator):
    """
    Returns an iterator that yields one sentence at a time from test data
    """
    current_sentence = [] #Buffer for the current sentence
    for l in corpus_iterator:
            if l==None:
                if current_sentence:  #Reached the end of a sentence
                    yield current_sentence
                    current_sentence = [] #Reset buffer
                else: # Got empty input stream
                    sys.stderr.write("WARNING: Got empty input file/stream.\n")
                    raise StopIteration
            else:
                current_sentence.append(l) #Add token to the buffer

    if current_sentence: # If the last line was blank, we're done
        yield current_sentence  #Otherwise when there is no more token
                                # in the stream return the last sentence.

def get_trigrams(sent_iterator):
    """
    Get a generator that returns trigrams over the entire corpus,
    respecting sentence boundaries and inserting boundary tokens.
    Sent_iterator is a generator object whose elements are lists
    of tokens.
    """
    for sent in sent_iterator:
         #Add boundary symbols to the sentence
         w_boundary = (2) * ["*"]
         w_boundary.extend(sent)
         w_boundary.append("STOP")
         #Then extract trigrams
         ngrams = (tuple(w_boundary[i:i+3]) for i in xrange(len(w_boundary)-2))
         for n_gram in ngrams: #Return one n-gram at a time
            yield n_gram

def usage():
    print """
    python viterbi.py [counts_file] [input_file] > [output_file]
        Read in counts_file generated from training set and
        test set of data, then predict tags for each word in
        test set.

        Results are stored in the following format:

          <word> <tag> <log probability of tagged sequence up to this word>
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

    # Iterate over all sentences



    # Viterbi Algorithm

    # Initialize
    # K[0], K[-1] = "*", K[1...n] = all_states
    K = ["*"] + [counter.all_states] + ["*"]

    # pi[k](u,v) -- n by len(K[k])
    pi = [defaultdict(float) for i in xrange(counter.)]

    # pi[0]

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


