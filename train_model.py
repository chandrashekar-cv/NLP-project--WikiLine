import os
import cPickle as pickle
import glob
import math
import time

from lxml import etree

from GlobalModel import *
from CategoryModel import *
from preprocess import *
from utility import *

#### CONSTANTS AND OPTIONS DEFINED HERE
INPUT_FOLDER = "data"
MODEL_FOLDER = "model"
GLOBAL_MODEL_FILE = "global.pkl"

TF_K_VALUE = 1
TF_OPT = TF_DBL_NORM
ICF_OPT = ICF_INV_FREQ_MAX




def update_global_model(gm, words, categories):
	word_ids = []
	for word in words:
		# if("." in word):
		# 	print word
		word_ids.append(gm.update_word(word, categories))
	return gm, word_ids

def update_cat_model(cm_dict, word_ids, cat_id):
	#Check if the corresponing cat_id pickle file exists
	if(cat_id not in cm_dict):
		cm_dict[cat_id] = CategoryModel()
	#update article count
	cm_dict[cat_id].inc_num_article()
	#print len(words)
	for w_id in word_ids:
		cm_dict[cat_id].update_wc(w_id)
	
	return cm_dict



### Training ###
s_t = time.time()

gm = GlobalModel()
cm_dict = {}

for xml_file in glob.glob(os.path.join(INPUT_FOLDER,"*")):
	print xml_file
	tree = etree.parse(xml_file)
	root = tree.getroot()

	# Get tokens 
	words = preprocess_content(root.findtext('TEXT'), NLTK_TOKENIZE)

	# Get Categories
	categories = []
	for cat in root.find('CATEGORIES'):
		categories.append(cat.text)

	#Update Global Model
	gm, word_ids = update_global_model(gm, words, categories)

	for cat in categories:
		cm_dict = update_cat_model(cm_dict, word_ids, gm.get_category_id(cat))

e_t = time.time()
print "time taken for Training: " + str(e_t - s_t)


s_t = time.time()

# Score Calculation pass

# To set value of word appearing maximum categories
gm.set_max_word_cat_val()

for c in cm_dict:
	print "Updating score for category: ", c
	#To calculate max word ct
	cm_dict[c].update_max_wc()

	#Score calculation
	for word_id in cm_dict[c].wc_dict:
		#Format: calc_tf(n, max_n, opt, k) 
		#Format: calc_icf(n_t, max_n_t, N, opt)
		score = calc_tf(cm_dict[c].get_wc(word_id), cm_dict[c].get_max_wc(), TF_OPT, TF_K_VALUE) \
				* calc_icf(gm.get_num_cat_given_word(word_id), gm.get_max_word_cat_val(), gm.get_num_cat(), ICF_OPT)
		cm_dict[c].set_score(word_id, score)

	with open(os.path.join(MODEL_FOLDER, str(c)+'.pkl'), 'wb') as f:
		pickle.dump(cm_dict[c], f, protocol=-1)
	cm_dict[c] = None

# Update GlobalModel pickle
with open(os.path.join(MODEL_FOLDER, GLOBAL_MODEL_FILE), 'wb') as f:
	pickle.dump(gm, f, protocol=-1)

e_t = time.time()
print "time taken for Score calc: " + str(e_t - s_t)


