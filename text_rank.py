#TODO
#Tokenizacja dla Polskiego
#output, ile najbardziej kluczowych zdań wybrać?
#refactoring do igraph
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine
import numpy as np
import networkx as nx
import nltk
from nltk.probability import FreqDist
import os
from morfeusz import analyse
VectorMaker = TfidfVectorizer()

PATH_STOPWORDS = 'stopwords.txt'

def get_stopwords():
    file = open(PATH_STOPWORDS,'r',encoding='utf-8')
    read = file.read()
    list = read.split('\n')
    return list

#This function reads the file from a given location
def get_file(src_file):
    file_open = open(src_file, 'r', encoding='utf-8')
    file_read = file_open.read()
    file_read = file_read.lower()
    file_read = nltk.word_tokenize(file_read)
    file_read = [f for f in file_read if f not in get_stopwords()]
    file_read = [f for f in file_read if f.isalpha()]
    file_read = ' '.join(file_read)
    return file_read

#This function takes a given text, in which each line represents a single sentence
#A TFIDF transformation is done, and the output tfidf matrix is returned as a dense matrix (both the matrix and its transposition
def get_tfidf(doc):
    sentence_list = doc.split('\n')
    sentence_list = [s for s in sentence_list if len(s)>0]
    tfidf = VectorMaker.fit_transform(sentence_list)
    dense_tfidf = tfidf.todense()
    dense_tfidf = np.asarray(dense_tfidf)
    t_dense = dense_tfidf.transpose()
    return dense_tfidf, t_dense

#Function for calculating the sentence ranks
def get_ranks(mat, t_mat):
    dims = mat.shape
    similarities = np.zeros((dims[0], dims[0]))
    #calculate cosine similarities matrix between sentences
    for d in range(dims[0]):
        for e in range(dims[0]):
            similarities[d, e] = (1 - cosine(mat[d, :], t_mat[:, e]))
    #build graph for rank extraction

    graph = nx.from_numpy_matrix(similarities)
    #apply pagerank algorithm
    rank = nx.pagerank(graph)
    return rank

#extract a list of top most ranked sentences from a document
def get_ranked(ranks, sent_list, top_rank):
    x = ranks.values()
    x = list(x)
    x.sort(reverse=True)
    top = x[:top_rank]
    selected_ranks = []
    for key in ranks:
        for t in top:
            if ranks[key] == t:
                selected_ranks.append(key)
    text = [sent_list[t-1] for t in selected_ranks]
#    if len(text)>3:
#        results = [t[1].capitalize() + t[2:] for t in text]

    return text

#pipeline function
def main(file_name):
    intake = get_file(file_name)
    sents = get_tfidf(intake)
    current_ranks = get_ranks(sents[0], sents[1])
    return current_ranks
PATH = 'C:/Users/barto/Desktop/articles/'


def get_words(txt):
    words = nltk.word_tokenize(txt)
    words_1 = []
    for w in words:
        if analyse(w)[0][0][1] != None:
            words_1.append(analyse(w)[0][0][1])
        else:
            words_1.append(w)
    words_1 = [w for w in words_1 if len(w)>2]
    fdist = FreqDist(words_1)
    most = fdist.most_common(5)
    most = [m[0] for m in most]
    return most

for path in os.listdir(PATH):
#    try:
        sents = get_file(PATH+path).split('\n')
        sents = [s for s in sents if len(s)>0]
        output = get_ranked(main(PATH+path), sents, 3)
        txt = ' '.join(output)
        print(get_words(txt))

#    except:
#        print("fail")

