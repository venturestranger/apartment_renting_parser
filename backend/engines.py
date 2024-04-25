from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import WhitespaceSplit
from tokenizers.trainers import BpeTrainer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
# from keras.models import Sequential
# from keras.layers import LSTM, Dense, Input
from unidecode import unidecode
from .utils import AhoCorasick
from .utils import latinizeCorpora
import numpy as np
import pandas as pd


# Key words classifier
class KWC:
	def __init__(self, config):
		self.engine_name = 'KWC'
		self.adds = config.ADDS
		self.subs = config.SUBS
		self.threshold = config.THRESHOLD
		self.positive_matcher = AhoCorasick()
		self.negative_matcher = AhoCorasick()

		for sub in self.subs:
			self.negative_matcher.add_pattern(sub)
		self.negative_matcher.create_fail_links()

		for add in self.adds:
			self.positive_matcher.add_pattern(add)
		self.positive_matcher.create_fail_links()

	def predict(self, content):
		ret = np.zeros(len(content))

		for i in range(len(content)):
			ret[i] = 1 if self.positive_matcher.match_count(content[i].lower()) - self.negative_matcher.match_count(content[i].lower()) >= self.threshold else 0
		return ret


# Normalizer + tokenizer + vectorizer + naive bayes
class NTVNB:
	def __init__(self, config, corpora):
		self.engine_name = 'NTVNB'
		alphabet = config.ALPHABET
		self.tokenizer = Tokenizer(BPE())
		self.vocab_size = config.VOCAB_SIZE
		trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"], vocab_size=config.VOCAB_SIZE, max_token_length=config.MAX_TOKEN_LENGTH, initial_alphabet=[i for i in alphabet], limit_alphabet=len(alphabet))
		self.tokenizer.pre_tokenizer = WhitespaceSplit()
		
		if config.LATINIZE_CORPORA == True:
			corpora = latinizeCorpora(corpora)
			
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
			ret.append(self.__count(self.tokenizer.encode(unidecode(i.lower())).ids))
		return ret
	
	# Fits the model on the given data and targets
	def fit(self, data, target):
		dat = []
		for i in data:
			dat.append(unidecode(i.lower()))
		self.model.fit(self.__vectorize(dat), target)
	
	# Tokenizes a message
	def tokenize(self, content):
		return self.tokenizer.encode(unidecode(content.lower())).ids
	
	# Gives an estimation for a content provided
	def predict(self, content):
		return self.model.predict(self.__vectorize(content))


# Normalizer + tokenizer + vectorizer + random forest
class NTVRF:
	def __init__(self, config, corpora):
		self.engine_name = 'NTVRF'
		alphabet = config.ALPHABET
		self.tokenizer = Tokenizer(BPE())
		self.vocab_size = config.VOCAB_SIZE
		trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"], vocab_size=config.VOCAB_SIZE, max_token_length=config.MAX_TOKEN_LENGTH, initial_alphabet=[i for i in alphabet], limit_alphabet=len(alphabet))
		self.tokenizer.pre_tokenizer = WhitespaceSplit()
		
		if config.LATINIZE_CORPORA == True:
			corpora = latinizeCorpora(corpora)
			
		self.tokenizer.train(corpora, trainer)
		self.model = RandomForestClassifier(n_estimators=config.N_ESTIMATORS, max_depth=config.MAX_DEPTH)
	
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
			ret.append(self.__count(self.tokenizer.encode(unidecode(i.lower())).ids))
		return ret
	
	# Fits the model on the given data and targets
	def fit(self, data, target):
		dat = []
		for i in data:
			dat.append(unidecode(i.lower()))
		self.model.fit(self.__vectorize(dat), target)
	
	# Tokenizes a message
	def tokenize(self, content):
		return self.tokenizer.encode(unidecode(content.lower())).ids
	
	# Gives an estimation for a content provided
	def predict(self, content):
		return self.model.predict(self.__vectorize(content))
