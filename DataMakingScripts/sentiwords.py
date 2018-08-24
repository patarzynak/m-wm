import os
import nltk
import spacy
from nltk.corpus import sentiwordnet as sw

#Helper function to write all elements from a list into a file
def write_all(all, fname):
    with open(fname, 'w') as adj_list:
        for adj in all:
            line = adj + '\n'
            adj_list.write(line)

#Create lists of positive, negative, objective and all adjectives as per SentiWordnet. 
#Needs to be run once to create appropriate files, before 'make_gold' can be executed.
def make_lists():
    alladj = []
    pos = []
    neg = []
    obj = []
    for s in sw.all_senti_synsets():
        if s.synset.pos() in ['a', 's']:
            print(s.synset.lemma_names()[0])
            alladj.append(s.synset.lemma_names()[0])#+'/JJ')
            if s.pos_score() > s.neg_score():
                pos.append(s.synset.lemma_names()[0])#+'/JJ')
            elif s.pos_score() < s.neg_score():
                neg.append(s.synset.lemma_names()[0])#'/JJ')
            else:
                obj.append(s.synset.lemma_names()[0])#'/JJ')
        else:
            pass

    write_all(neg, "neglisttag.txt")
    write_all(pos, "poslisttag.txt")
    write_all(alladj, "alllisttag.txt")
    write_all(obj, "objlist.txt")

#Read a list from a file into a set
def read_into_set(fname):
    w_set = set()
    with open(fname) as file:
        for line in file:
            word = line.strip()
            w_set.add(word)
    return w_set

#Use a list of positive & negative adjectives (from Senti WordNet) to label adjectives found in reviews.
def make_gold():
    polar_set = set()
    pos_set = read_into_set("poslist.txt")
    neg_set = read_into_set("neglist.txt")
    polar_set = pos_set.union(neg_set)

    all_set = read_into_set("alllist.txt")
    directory = os.fsencode("./reviews/")
    labels = []
    for file in os.listdir(directory):
        fname = str(file)
        score = fname.replace('.', '_').split("_")[1]
        id = fname.replace('\'', '.').split(".")[1]
        print(fname)
        print(score)
        with open(directory+file) as f:
            for line in f:
                tokens = line.split(' ')
                #text = nltk.word_tokenize(line)
                tags = nltk.pos_tag(tokens)
                char_count = 0
                for tag in tags:
                    word = tag[0]
                    pos = tag[1]
                    if word in all_set and pos == "JJ":
                        if word in polar_set: # < here use the set for which you want to create a "gold"annotation 
                            print(word)
                            print(line[char_count])
                            labeloo = id + "::span:" + str(char_count) + ":" + str(char_count + len(word) - 1) + "\t1"
                            labels.append(labeloo)
                        else:
                            print(word)
                            labeloo = id + "::span:" + str(char_count) + ":" + str(char_count + len(word) - 1) + "\t-1"
                            labels.append(labeloo)
                    char_count = char_count + len(word) + 1
                '''
                for word in tokens:
                    if word in all_set:
                        if word in pos_set:
                            #TODO:calculate position
                            print(word)
                            print(line[char_count])
                            labeloo = id + "::span:" + str(char_count) + ":" + str(char_count + len(word)-1) + "\t1"
                            labels.append(labeloo)
                        else:
                            print(word)
                            labeloo = id + "::span:" + str(char_count) + ":" + str(char_count + len(word) - 1) + "\t-1"
                            labels.append(labeloo)
                        char_count = char_count + len(word) + 1
                '''

    #Insert the name of the new file, where the gold data should be saved
    with open('gold_senti_polar.tsv', 'a') as gold_file:
        for label in labels:
            line = label + "\n"
            gold_file.write(line)

#UNUSED - the function to create a pre-tagged version of reviews - done before the spacy parsing of snorkel was used, no longer and probably doesn't work
def pos_tag():
    spacy.download('en')
    nlp = spacy.load('~/models/en_core_web_sm-2.1.0a0/en_core_web_sm//en_core_web_sm-2.1.0a0')
    #doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')
    r_directory = os.fsencode("./reviews/")
    w_directory = "./reviews2/"
    for file in os.listdir(r_directory):
        fname = str(file).strip('\'b')
        with open(r_directory+file) as f:
            new_text = ""
            for line in f:
                text = nltk.word_tokenize(line)
                tags = nltk.pos_tag(text)
                new_line = ''
                for tag in tags:
                    sym = tag[0] + '/' + tag[1]
                    new_line = new_line + sym + ' '
                new_line += '\n'
            new_text += new_line
        #with open(fname, 'w+') as f2:
            #f2.write(str(new_text))


def main():
    #make_lists()
    make_gold()


if __name__ == "__main__":
    main()
