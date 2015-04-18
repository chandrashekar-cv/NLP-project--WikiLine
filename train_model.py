import os
import cpickle as pickle
import glob
import math

from lxml import etree
import nltk

from GlobalModel import *
from CategoryModel import *

#### CONSTANTS AND OPTIONS DEFINED HERE
INPUT_FOLDER = ""
MODEL_FOLDER = ""
GLOBAL_MODEL_FILE = "global.pickle"
WORD_PREPROCESS = 1

TF_K_VALUE = 1
TF_OPT = TF_DBL_NORM
ICF_OPT = ICF_INV_FREQ_MAX

#Preprocessing logic will be put here
def preprocess_content(content, opt):
	# More options can be put here
	if(opt == 1):
		return nltk.word_tokenize(content)
	else:
		return content.split()


def update_global_model(gm, words, categories):
	if(gm == None):
		gm = GlobalModel()
		
	for word in words:
		gm.update_word(word, categories)

	return gm


def update_cat_model(words, cat_id):
	#Check if the corresponing cat_id pickle file exists
	if(not os.path.isfile(os.path.join(MODEL_FOLDER, str(i)+'.pickle'))):
		cm = CategoryModel()
		with open(os.path.join(MODEL_FOLDER, str(i)+'.pickle')), 'wb') as f:
			pickle.dump(cm, f, protocol=-1)
	
	cm = None
	with open(os.path.join(MODEL_FOLDER, str(i)+'.pickle')), 'wb') as f:
		cm = pickle.load(f)

		for word in words:
			cm.update_dict(word)

		pickle.dump(cm, f, protocol=-1)
	return

### Training ###

gm = None

# Pass on complete Data
for xml_file in glob.glob(os.path.join(INPUT_FOLDER,"/*")):
	tree = etree.parse(xml_file)
	root = tree.getroot()

	# Get tokens 
	words = preprocess_content(root.findtext('TEXT'), WORD_PREPROCESS)

	# Get Categories
	categories = []
	for cat in root.find('CATEGORIES'):
		categories.append(cat.text)

	#Update Global Model
	gm = update_global_model(gm, words, categories)

	for cat in categories:
		update_cat_model(words, gm.get_category_id(cat))



# Score Calculation pass

# To set value of word appearing maximum categories
gm.set_max_word_cat_val()

for i in range(gm.get_num_cat()):
	with open(os.path.join(MODEL_FOLDER, str(i+1)+'.pickle')), 'wb') as f:
		cm = pickle.load(f)

		#To calculate max word ct
		cm.update_max_wc()

		#Score calculation
		for word in cm.word_dict:
			#Format: calc_tf(n, max_n, opt, k) 
			#Format: calc_icf(n_t, max_n_t, N, opt)
			score = calc_tf(cm.get_word_count(word), cm.get_max_wc(), TF_OPT, TF_K_VALUE) \
					* calc_icf(gm.get_num_cat_given_word(word), gm.get_max_word_cat_val(), gm.get_num_cat(), ICF_OPT)
			cm.set_tf_idf_dict(score)

		pickle.dump(cm, f, protocol=-1)


# Update GlobalModel pickle
with open(os.path.join(MODEL_FOLDER, GLOBAL_MODEL_FILE), 'wb') as f:
	pickle.dump(gm, f, protocol=-1)



