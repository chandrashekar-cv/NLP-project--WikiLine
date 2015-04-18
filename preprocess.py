import nltk

#Options
NLTK_TOKENIZE =  0

#Preprocessing logic will be put here
def preprocess_content(content, opt):
	# More options can be put here
	if(opt == NLTK_TOKENIZE):
		return nltk.word_tokenize(content)
	else:
		return content.split()