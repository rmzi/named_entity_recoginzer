# COMSW4705 - NLP HW#1
#
# Run HW1, generate files for grading
# Writeup in the README
#
# Author: Ramzi Abdoch

# Make output dir, copy ner_train.dat for later use
mkdir output
cp ner_train.dat output/ner_train.dat
cp ner_train.dat output/ner_train_grouped.dat

# Run Question #4
python count_freqs.py output/ner_train.dat > output/ner.counts
python replace_rare.py output/ner.counts output/ner_train.dat
python count_freqs.py output/ner_train.dat > output/ner_rare.counts
python tagger.py output/ner_rare.counts ner_dev.dat > output/tagger_preds.dat
python eval_ne_tagger.py ner_dev.key output/tagger_preds.dat

# Run Question #5
python viterbi.py output/ner_rare.counts ner_dev.dat > output/viterbi_preds.dat
python eval_ne_tagger.py ner_dev.key output/viterbi_preds.dat

# Run Question #6
python count_freqs.py output/ner_train_grouped.dat > output/ner.counts
python group_rare.py output/ner.counts output/ner_train_grouped.dat
python count_freqs.py output/ner_train_grouped.dat > output/ner_grouped_rare.counts
python viterbi_grouped.py output/ner_grouped_rare.counts ner_dev.dat > output/grouped_viterbi_preds.dat
python eval_ne_tagger.py ner_dev.key output/grouped_viterbi_preds.dat
