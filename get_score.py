## Python wrapper function to get score 
import os
import cPickle as pickle

from GlobalModel import *
from CategoryModel import *
from preprocess import *

MODEL_FOLDER = "model"
GLOBAL_MODEL_FILE = "global.pkl"


def get_scores(sentences, cat):
    scores, gm = [], None
    
    #Load gm
    with open(os.path.join(MODEL_FOLDER, GLOBAL_MODEL_FILE), 'rb') as f:
        gm = pickle.load(f)
        #Load cm
        with open(os.path.join(MODEL_FOLDER, str(gm.get_category_id(cat)) +'.pkl'), 'rb') as f:
            cm = pickle.load(f)
            #If article count is <= 1
            if(cm.get_num_article() <= 1):
                return None

            for s in sentences:
                score = 0
                for w in preprocess_content(s, NLTK_TOKENIZE):
                    score += cm.get_score(gm.get_word_id(w))
                scores.append(score)

    return scores 
    
