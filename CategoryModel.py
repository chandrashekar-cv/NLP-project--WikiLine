'''
This CategoryModel object will be created for every Wikipedia Category

'''

class CategoryModel(object): 
	
	def __init__():
		
		# Total num of tokens in category (In case we need to normalize the term frequency)
		num_token = 0
		
		# Max value of word count
		max_wc = -1

		# Initialize the word count dictionary
		word_dict = {}

		# Initialize tf idf dict (To be calculated in the end)
		tf_idf_dict = {}
		

	def update_dict(word):
		self.num_token += 1
		if(word in self.word_dict):
			self.word_dict[word] += 1
		else:
			self.word_dict[word] = 1
		return

	def get_word_count(word):
		if(word in self.word_dict):
			return self.word_dict[word]
		else:
			return 0

	def set_tf_idf_dict(word, tf_idf_score):
		self.tf_idf_dict[word] = tf_idf_score
		return

	def get_tf_idf_score(word):
		if(word in self.tf_idf_dict):
			return self.tf_idf_dict[word]
		else:
			return 0

	#To be run in the end
	def update_max_wc():
		for word in self.word_dict:
			if(self.word_dict[word] > self.max_wc):
				self.max_wc = self.word_dict[word]
		return

	def get_max_wc():
		if(self.max_wc == -1):
			raise Exception("Max wc not yet calculated")
			return -1
		else:
			return self.max_wc




	