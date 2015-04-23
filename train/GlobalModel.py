"""
Required for calculating ICF (Inverse Category Frequency)

"""

class GlobalModel(object):
	
	def __init__(self):

		# Category Counter
		self.num_cat = 0

		# Word Counter
		self.num_word = 0

		#Max word cat value
		self.max_word_cat_val = -1
		
		# Category ("category string" => id) dictionary
		self.cat_dict = {}

		# Word dictionary ("word string" => id)
		self.word_dict = {}

		# word_cat dictionary ("word string" => {(cat_id1:true) (cat_id2:true) ... })
		self.word_cat_dict = {}


	def update_word(self, word, categories):
		"""
		: @param: word (type String) -> word name
		: @param: categ (type List[String]) -> Category list
		"""
		for cat in categories:

			cat_id = self.get_category_id(cat)
			#check if category is not present in cat_dict, update it
			if(cat_id == -1):
				cat_id = self.set_category_id(cat)

			word_id = self.get_word_id(word)

			#check if word is not present in word_dict, update it and also update word_cat dict
			if(word_id == -1):
				word_id = self.set_word_id(word)
				self.word_cat_dict[word_id] = {}

			self.word_cat_dict[word_id][cat_id] = True
		return word_id

	def set_word_id(self, word):
		self.num_word += 1
		self.word_dict[word] = self.num_word 
		return self.num_word


	def get_word_id(self, word):
		if(word in self.word_dict):
			return self.word_dict[word]
		else:
			return -1

	def set_category_id(self, cat):
		self.num_cat += 1
		self.cat_dict[cat] = self.num_cat
		return self.num_cat


	def get_category_id(self, cat):
		if(cat in self.cat_dict):
			return self.cat_dict[cat]
		else:
			return -1

	def get_num_word(self):
		return self.num_word

	def get_num_cat(self):
		return self.num_cat

	def get_num_cat_given_word(self, word):
		#print word
		if(word not in self.word_cat_dict):
			#print("not in word_cat_dict")
			return 0
		else:
			return len(self.word_cat_dict[word])

	#To be called in the end
	def set_max_word_cat_val(self):
		for word in self.word_cat_dict:
			if(len(self.word_cat_dict[word]) > self.max_word_cat_val):
				self.max_word_cat_val = len(self.word_cat_dict[word])

		return

	def get_max_word_cat_val(self):
		if(self.max_word_cat_val == -1):
			raise Exception("Max word category value not yet set")
			return -1
		else:
			#print self.max_word_cat_val
			return self.max_word_cat_val

