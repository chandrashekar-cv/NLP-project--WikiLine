"""
Required for calculating ICF (Inverse Category Frequency)

"""

class GlobalModel(object):
	
	def __init__():

		# Category Counter
		num_cat = 0

		#Max word cat value
		max_word_cat_val = -1
		
		# Category ("category string" => id) dictionary
		cat_dict = {}

		# word_cat dictionary ("word string" => {(cat_id1:true) (cat_id2:true) ... })
		word_cat_dict = {}


	def update_word(word, categories):
		"""
		: @param: word (type String) -> word name
		: @param: categ (type List[String]) -> Category list
		"""
		for cat in categories:

			#check if category is not present in cat_dict, update it
			if(cat not in self.cat_dict):
				self.num_cat += 1
				self.cat_dict[cat] = self.num_cat
			
			#check if word is not present in word_cat_dict, update it
			if(word not in self.word_cat_dict):
				self.word_cat_dict[word] = {} 

			self.word_cat_dict[cat] = True

			#Thats all i suppose :P

	def get_category_id(category):
		if(cat in self.cat_dict):
			return self.cat_dict[cat]
		else
			return -1

	def get_num_cat():
		return self.num_cat

	def get_num_cat_given_word(word):
		if(word not in self.word_cat_dict):
			return 0
		else:
			return len(self.word_cat_dict[word])

	#To be called in the end
	def set_max_word_cat_val():
		for word in self.word_cat_dict:

			if(len(self.word_cat_dict[word]) > self.max_word_cat_val):
				self.max_word_cat_val = len(self.word_cat_dict[word])

		return

	def get_max_word_cat_val():
		if(self.max_word_cat_val == -1):
			raise Exception("Max word category value not yet set")
			return -1
		else:
			return self.max_word_cat_val

