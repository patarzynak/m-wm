#####This is the file I used for turning the CW corpus into a word list and getting features for these words

import csv
import random
from nltk.corpus import wordnet as wn

freq_dictionary = dict()


def get_features(word):
    # word length
    wl = str(len(word))

    # word frequency
    try:
        freq = freq_dictionary[word]
    except:
        freq = 0

    # number of synsets in WordNet
    synsets = wn.synsets(word)
    no_s = str(len(synsets))

    feats = word + ' ' + wl + ' ' + no_s + ' ' + str(freq)
    return feats


def main():
    simples = set()
    complexs = set()
    with open('cwcorpus.txt', encoding='iso-8859-1') as corpus:
        corpus.readline()
        for line in corpus:
            line = line.strip()
            example = line.split('\t')
            # print(example)
            index = int(example[1]) - 1
            simple = example[2]
            sentence = example[3]
            sentence = sentence.split()
            complex = sentence[index]
            # print(simple, complex)
            simples.add(simple)
            complexs.add(complex)
    print(len(simples))
    print(len(complexs))

    print(simples.intersection(complexs))

    label_dictionary = dict()

    for e in complexs:
        label_dictionary[e] = 1
    for e in simples:
        label_dictionary[e] = -1
    '''
    with open('freqlist.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        next(reader)
        for row in reader:
            word = row[1].strip()
            freq_dictionary[word] = str(row[0])
            # print(word, freq_dictionary[word])
    '''
    with open('all.al', 'r') as bnc:
        for line in bnc:
            attributes = line.split()
            word = attributes[1]
            count = int(attributes[0])
            if word in freq_dictionary.keys():
                freq_dictionary[word] += count
            else:
                freq_dictionary[word] = count

    idx = 0
    feature_dictionary = dict()
    gold_dictionary = dict()
    with open('wordlist', 'r') as wordlist:
        for line in wordlist:
            word = line.strip()
            feats = get_features(word)
            ID = "{0:0=4d}".format(idx)
            feature_dictionary[ID] = feats
            idx += 1

    for key, value in label_dictionary.items():
        word = key
        feats = get_features(word)
        ID = "{0:0=4d}".format(idx)
        feature_dictionary[ID] = feats
        gold_dictionary[ID] = (len(word), label_dictionary[word])
        idx += 1

    print(gold_dictionary)
    print(feature_dictionary)
    key_list = list(feature_dictionary.keys())
    random.shuffle(key_list)

    ix = 0
    with open('corpus.txt', 'a') as new_corpus:
        for key, value in feature_dictionary.items():
            line = key + '\t' + value + '\n'
            new_corpus.write(line)

    with open('gold.tsv', 'a') as label_file:
        for key in gold_dictionary:
            tup = gold_dictionary[key]
            bound = tup[0] - 1
            lab = tup[1]
            line = key + '::span:0:' + str(bound) + '\t' + str(lab) + '\n'
            label_file.write(line)

        '''
            feats = get_features(e, ix)
            ix += 1
            label = '0'
            line = feats + label + '\n'
            new_corpus.write(line)
        for e in complexs:
            feats = get_features(e, ix)
            ix += 1

            label = '1'
            line = feats + label + '\n'
            new_corpus.write(line)
            '''

if __name__ == "__main__":
    main()
