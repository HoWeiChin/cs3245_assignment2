#!/usr/bin/python
import re
import nltk
import sys
import getopt
import os
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

#for code development
trng_dir = 'C:/Users/Wei Chin/Desktop/CS3245/HW #2/reuters/reuters/training'

set_stopwords = set(stopwords.words('english'))
punc = "[.,?!'\";:-]"
#initialised inverted_index, key == words, value = posting list
inverted_index = {}


#preprocess token_list, return a preprocessed set of words (unique word tokens)
def process_token_list(token_list):
    ps = PorterStemmer()
    processed_set = set()

    for token in token_list:
        #skip numbers
        if token.isdigit():
            continue
        #skip stop words
        if token in set_stopwords:
            continue
        #skip punctuation tokens
        if token in punc:
            continue
        else:
            #stem a word token 
            processed_token = ps.stem(token)
            processed_set.add(processed_token)
    return processed_set


#preprocess line, return a preprocessed set of words 
def process_line(line):
    #convert everything to lowercase
    line = line.lower()
    #tokenize line
    token_list = word_tokenize(line)
    processed_words_set = process_token_list(token_list)
    return processed_words_set

        
#preprocess a reuters_doc, return a set of words perculiar to that document
def process_reuters_file(reuters_doc):
    f = open(reuters_doc, 'r')
    word_set_in_doc = set()
    for line in f:
        #get set of words obtained from that line
        words_set_in_line = process_line(line)
        for word in words_set_in_line:
            word_set_in_doc.add(word)
    return word_set_in_doc

#populate inverted_index with set of words for each reuters document
def populate_index(doc_word_set, docID):
    for word in doc_word_set:
        if word not in inverted_index:
            inverted_index[word] = [docID]
        else:
            inverted_index[word].append(docID)
            


def index(reuters_dir, dic_file, post_file):
    reuters_file_lst = sorted(os.listdir(reuters_dir))
    for doc in reuters_file_lst:
        #get full path of doc
        doc = os.path.join(reuters_dir, doc)
        #get set of words from that doc
        doc_word_set = process_reuters_file(doc)
        #populate inverted_index with doc_word_set and that particular docID
        populate_index(doc_word_set, doc)
    
    #write output file for dictionary
    d_f = open(dic_file, 'w+')
    for term in inverted_index:
        line = term + '\n'
        d_f.write(line)
    d_f.close()

    #write output file for postings
    p_f = open(post_file, 'w+')
    for p_lst in inverted_index.values():
        line = str(p_lst) + '\n'
        p_f.write(line)
    p_f.close()



    
    

        

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError as err:
    usage()
    sys.exit(2)
    
for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

        
if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)









