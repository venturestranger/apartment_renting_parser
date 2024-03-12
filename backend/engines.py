from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import WhitespaceSplit
from tokenizers.trainers import BpeTrainer
from sklearn.naive_bayes import MultinomialNB
from unidecode import unidecode
import numpy as np
import pandas as pd

# Normalizer + tokenizer + vectorizer + naive bayes
class NTVNB:
	def __init__(self, config, corpora):
		self.engine_name = 'NTVNB'
		alphabet = config.ALPHABET
		self.tokenizer = Tokenizer(BPE())
		self.vocab_size = config.VOCAB_SIZE
		trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"], vocab_size=config.VOCAB_SIZE, max_token_length=config.MAX_TOKEN_LENGTH, initial_alphabet=[i for i in alphabet], limit_alphabet=len(alphabet))
		self.tokenizer.pre_tokenizer = WhitespaceSplit()
		self.tokenizer.train(corpora, trainer)
		self.model = MultinomialNB()
	
	# Converts an array of tokens into a bag of tokens
	def __count(self, data):
		ret = np.zeros(self.vocab_size)
		for i in data:
			ret[i] += 1
		return ret
	
	# Converts a string into a vector
	def __vectorize(self, data):
		ret = []
		for i in data:
			ret.append(self.__count(self.tokenizer.encode(unidecode(i)).ids))
		return ret
	
	# Fits the model on the given data and targets
	def fit(self, data, target):
		dat = []
		for i in data:
			dat.append(unidecode(i))
		self.model.fit(self.__vectorize(data), target)
	
	# Gives an estimation for a content provided
	def predict(self, content):
		return self.model.predict(self.__vectorize(content))

