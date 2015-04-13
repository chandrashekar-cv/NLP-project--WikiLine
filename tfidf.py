import sys
from collections import defaultdict
import nltk
from nltk.util import ngrams
import math
import pickle
import operator

inverted_index = defaultdict(dict)
idf_index = defaultdict(int)
stop_words = nltk.corpus.stopwords.words('english')

def term_frequency(document, document_id):
    features = nltk.word_tokenize(document)
    bigrams = ngrams(features, 2)
    for feature in features:
        if feature not in stop_words:
            inverted_index[feature][document_id] = inverted_index[feature].get(document_id, 0) + 1
    for bigram in bigrams:
        inverted_index[bigram][document_id] = inverted_index[feature].get(document_id, 0) + 1

def get_idf(term, total_documents):
    return math.log(total_documents/len(inverted_index[term]))    

def update_weights(total_documents):
    for term in inverted_index:
        for doc in inverted_index[term]:
            idf = get_idf(term, total_documents)
            inverted_index[term][doc] *= idf


def get_tf_idf(term):
    return inverted_index[term]

def store(file_name):
    output = open(file_name, 'wb')
    pickle.dump(inverted_index, output)
    output.close()

def load(file_name):
    pkl_file = open(file_name, 'rb')
    inverted_index = pickle.load(pkl_file)
    pkl_file.close()

def get_relevant_documents(query):
    documents = defaultdict(float)
    features = nltk.word_tokenize(query)
    bigrams = ngrams(features, 2)
    for feature in features:
        feature_vector = inverted_index[feature]
        for doc in feature_vector:
            documents[doc] += feature_vector[doc]

    sorted_documents = sorted(documents.items(), key = operator.itemgetter(1))    
    print(sorted_documents)
    
    
    
     
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("python3 tfidf.py")
        print("either 1 input_file")
        print("or 2 <query>")
        sys.exit(-1)
    
    term_frequency("Hello program", "1") 
    term_frequency("Hello world", "2") 
    update_weights(2)
    #print(inverted_index)
    store("inverted_index.pkl")
    load("inverted_index.pkl")
    print(inverted_index)
    get_relevant_documents("world")
