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
INPUT_FOLDER = "sample"
MODEL_FOLDER = "model"
GLOBAL_MODEL_FILE = "global.pkl"

TF_K_VALUE = 1
TF_OPT = TF_DBL_NORM
ICF_OPT = ICF_INV_FREQ_MAX




def update_global_model(gm, words, categories):
	
	for word in words:
		gm.update_word(word, categories)

	return gm


def update_cat_model(words, cat_id):
	#Check if the corresponing cat_id pickle file exists
	if(not os.path.isfile(os.path.join(MODEL_FOLDER, str(cat_id)+'.pkl'))):
		
		with open(os.path.join(MODEL_FOLDER, str(cat_id)+'.pkl'), 'wb') as f:
			cm = CategoryModel()
			pickle.dump(cm, f, protocol=-1)
			#print "dump successful"
	
	cm = None
	with open(os.path.join(MODEL_FOLDER, str(cat_id)+'.pkl'), 'rb') as f:
		cm = pickle.load(f)

	#print len(words)
	for word in words:
		cm.update_wc(word)
	
	with open(os.path.join(MODEL_FOLDER, str(cat_id)+'.pkl'), 'wb') as f:
		pickle.dump(cm, f, protocol=-1)
	
	return

### Training ###
s_t = time.time()

gm = GlobalModel()

# ctr = 0
# Pass on complete Data
for xml_file in glob.glob(os.path.join(INPUT_FOLDER,"*")):
	# if(ctr == 100):
	# 	break
	# print ctr
	# ctr += 1
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
	gm = update_global_model(gm, words, categories)

	for cat in categories:
		update_cat_model(words, gm.get_category_id(cat))

e_t = time.time()
print "time taken for Training: " + str(e_t - s_t)


s_t = time.time()

# Score Calculation pass

# To set value of word appearing maximum categories
gm.set_max_word_cat_val()

for i in range(gm.get_num_cat()):
	cm = None
	with open(os.path.join(MODEL_FOLDER, str(i+1)+'.pkl'), 'rb') as f:
		cm = pickle.load(f)

	#To calculate max word ct
	cm.update_max_wc()

	#Score calculation
	for word in cm.wc_dict:
		#Format: calc_tf(n, max_n, opt, k) 
		#Format: calc_icf(n_t, max_n_t, N, opt)
		if(word == 'captains'):
			print "captains"
			print calc_tf(cm.get_wc(word), cm.get_max_wc(), TF_OPT, TF_K_VALUE)
			print calc_icf(gm.get_num_cat_given_word(word), gm.get_max_word_cat_val(), gm.get_num_cat(), ICF_OPT)
		
		score = calc_tf(cm.get_wc(word), cm.get_max_wc(), TF_OPT, TF_K_VALUE) \
				* calc_icf(gm.get_num_cat_given_word(word), gm.get_max_word_cat_val(), gm.get_num_cat(), ICF_OPT)
		cm.set_score(word, score)

	with open(os.path.join(MODEL_FOLDER, str(i+1)+'.pkl'), 'wb') as f:
		pickle.dump(cm, f, protocol=-1)


# Update GlobalModel pickle
with open(os.path.join(MODEL_FOLDER, GLOBAL_MODEL_FILE), 'wb') as f:
	pickle.dump(gm, f, protocol=-1)

e_t = time.time()
print "time taken for Score calc: " + str(e_t - s_t)


