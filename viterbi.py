#! /usr/bin/python

__author__="Ramzi Abdoch <raa2148@olumbia.edu>"
__date__ ="$Feb 19, 2015"

import sys
import operator
import math
import itertools

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
        else:
            yield None
        l = corpus_file.readline()

def sent_iterator(word_iterator):
    """
    Returns an iterator that yields one sentence at a time from test data
    """
    current_sentence = [] #Buffer for the current sentence
    for l in word_iterator:
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

def usage():
    print """
    python viterbi.py [counts_file] [test_file] > [output_file]
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

    # Iterate over all test sentences
    test_sent_iterator =  sent_iterator(word_iterator(test_file))
    for sentence in test_sent_iterator:
        # Viterbi Algorithm
        n = len(sentence)

        pad_sent = (2) * ["*"]
        pad_sent.extend(sentence)
        pad_sent.append("STOP")

        # Initialize
        # K[0], K[-1] = "*", K[1...n] = all_states
        K = ["*"] + (n) * [counter.all_states] + ["*"]

        # pi[k](u,v) -- n by len(K[k])
        pi = [defaultdict(float) for i in xrange(n + 1)]

        # pi[0](u,v)
        pi[0][("*","*")] = 1.0

        # Assign all values in pi table
        for k in xrange(1, n+1):

            word = pad_sent[k+1]
            original_word = pad_sent[k+1]

            # Check if word is absent in training set or count(word) < 5, if so, use _RARE_
            if word not in counter.all_words or counter.word_counts[word] < 5:
                word = "_RARE_"

            for u in K[k-1]:
                for v in K[k]:

                    # Find max over w in K[k-2]
                    w_candidates = defaultdict(float)

                    for w in K[k-2]:
                        w_candidates[w] = pi[k-1][(w,u)] * counter.calc_mle([w,u,v]) * counter.calc_emissions(word,v)

                    final_w = max(w_candidates.iteritems(), key=operator.itemgetter(1))

                    # Assign pi value
                    pi[k][(u,v)] = final_w[1]

            # Get the (tag, probability) of v in max(pi[k](u,v))
            final_k_idx = max(pi[k].iteritems(), key=operator.itemgetter(1))

            prob = final_k_idx[1]
            # Log probability
            log_prob = math.log(prob)
            # Ouput format: word, tag, log probability
            sys.stdout.write("%s %s %s\n" % (original_word, final_k_idx[0][1], log_prob))

        # Find final max over u, v
        final_candidates = defaultdict(float)

        # Permute each pair of values for u in K[n-1] v and K[n-2]
        perms = itertools.product(K[n-1], K[n])

        # Iterate through permutations and calculate pi values
        for perm in perms:
            final_candidates[perm] = pi[n][perm] * counter.calc_mle(list(perm + ("STOP",)))

        # Calculate final probability for the sentence
        # ** Do not output to predictions file **
        final_sent_prob_idx = max(final_candidates.iteritems(), key=operator.itemgetter(1))

        print ""


