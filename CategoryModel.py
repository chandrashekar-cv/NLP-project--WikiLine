'''
This CategoryModel object will be created for every Wikipedia Category

'''

class CategoryModel(object): 
	
	def __init__(self):
		
		# Total num of tokens in category (In case we need to normalize the term frequency)
		self.num_token = 0
		
		# Max value of word count
		self.max_wc = -1

		# Initialize the word count dictionary
		self.wc_dict = {}

		# Initialize tf icf dict (To be calculated in the end)
		self.score_dict = {}
		

	def update_wc(self, word):
		self.num_token += 1
		if(word in self.wc_dict):
			self.wc_dict[word] += 1
		else:
			self.wc_dict[word] = 1
		return

	def get_wc(self, word):
		if(word in self.wc_dict):
			return self.wc_dict[word]
		else:
			return 0

	def set_score(self, word, score):
		self.score_dict[word] = score
		return

	def get_score(self, word):
		if(word in self.score_dict):
			return self.score_dict[word]
		else:
			return 0

	#To be run in the end
	def update_max_wc(self):
		for word in self.wc_dict:
			if(self.wc_dict[word] > self.max_wc):
				self.max_wc = self.wc_dict[word]
		return

	def get_max_wc(self):
		if(self.max_wc == -1):
			raise Exception("Max wc not yet calculated")
			return -1
		else:
			return self.max_wc




	