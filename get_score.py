## Python wrapper function to get score 
import sys, os
sys.path.append(os.path.join(os.getcwd(),'train'))
import cPickle as pickle


from GlobalModel import *
from CategoryModel import *
from preprocess import *

MODEL_FOLDER = "train/model/"
GLOBAL_MODEL_FILE = "global.pkl"
PART_GLOBAL_MODEL_FILE = "global_part.pkl"

def get_scores(sentences, cat):
    scores, cat_dict, gm = [], None, None
    
    #Load gm
    with open(os.path.join(MODEL_FOLDER, PART_GLOBAL_MODEL_FILE), 'rb') as f:
        gm = pickle.load(f)
        #gm.word_cat_dict = {}
        #print "Global model loaded"
        # with open(os.path.join(MODEL_FOLDER, ), 'wb') as f1:
        #     pickle.dump(gm, f1, protocol=-1)
        
        with open(os.path.join(MODEL_FOLDER, str(gm.get_category_id(cat)) +'.pkl'), 'rb') as f2:
            cm = pickle.load(f2)
            #If article count is <= 1
            if(cm.get_num_article() <= 1):
                return None

            for s in sentences:
                score = 0
                for w in preprocess_content(s, NLTK_TOKENIZE):
                    score += cm.get_score(gm.get_word_id(w))
                scores.append(score)

    return scores

#print get_scores(["hi this is great", "fantastic job"], "1984 births") 
    
