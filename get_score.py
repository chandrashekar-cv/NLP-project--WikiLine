## Python wrapper function to get score 
import os
import cPickle as pickle

from GlobalModel import *
from CategoryModel import *

MODEL_FOLDER = "model"
GLOBAL_MODEL_FILE = "global.pkl"


def get_score_given_word_cat(word, cat):
	score = -1
	with open(os.path.join(MODEL_FOLDER, GLOBAL_MODEL_FILE), 'rb') as f:
		gm = pickle.load(f)
		with open(os.path.join(MODEL_FOLDER, str(gm.get_category_id(cat)) +'.pkl'), 'rb') as f:
			cm = pickle.load(f)
			score = cm.get_score(word)
	if(score == -1):
		raise Exception ("Couldn't fetch score")
	return score