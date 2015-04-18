import nltk

#Preprocessing logic will be put here
def preprocess_content(content, opt):
	# More options can be put here
	if(opt == 1):
		return nltk.word_tokenize(content)
	else:
		return content.split()