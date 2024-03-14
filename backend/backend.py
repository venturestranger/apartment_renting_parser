import pandas as pd
import pickle

if __name__=='__main__':
	from config import Config
	from engines import NTVNB
	from engines import KWC
else:
	from .config import Config
	from .engines import NTVNB
	from .engines import KWC


# Implements an API interface
class API:
	def __init__(self):
		pass

	# Initializes a new engine (predicting model) or loads one from <engine_dir>
	def connect(self, engine_type='NTVNB', engine_types=[], engine_path=None, optional={}):
		if engine_path != None:
			try:
				with open(engine_path, 'rb') as f:
					self.engines = pickle.load(f)
			except:
				raise Exception('Error while loading the engine')
		else:
			self.engines = []
			if len(engine_types) == 0:
				engine_types = [engine_type]

			for engine in engine_types:
				match engine:
					case 'NTVNB':
						self.engines.append(NTVNB(Config.engine_configs[engine], optional['corpora']))
					case 'KWC':
						self.engines.append(KWC(Config.engine_configs[engine]))
					case e:
						raise Exception(f'{e} engine cannot be initialized')
	
	# Dumps the used engine
	def dump_engine(self, engine_path=None):
		try:
			with open(engine_path, 'wb') as f:
				pickle.dump(self.engines, f)
		except:
			raise Exception('Create an engine first')
	
	# Gives information on how many data points in a given dataset are positive or negative
	def dataset_stats(self, dataset_path):
		df = pd.read_csv(dataset_path)
		stat = {
			'pos': 0,
			'neg': 0,
		}

		try:
			stat['pos'] = len(df[df['y'] > 0.5])
			stat['neg'] = len(df[df['y'] <= 0.5])
		except:
			raise Exception('Referenced dataset should contain "y" column')
		else:
			return stat
	
	# Updates a given dataset with new data points
	def dataset_update(self, data_points, dataset_path):
		df = pd.read_csv(dataset_path)

		try:
			new = pd.DataFrame(data_points, columns=['x', 'y'])
			df = pd.concat([df, new])
		except:
			raise Exception('Data points should have only "x" and "y" columns')
		else:
			df.to_csv(dataset_path)

	# Retrains the engine on a given dataset
	def train(self, dataset_path):
		df = pd.read_csv(dataset_path)

		if 'x' in df.columns and 'y' in df.columns:
			for engine in self.engines:
				try:
					engine.fit(df['x'], df['y'])
				except:
					print(f'{engine.engine_name} not trainable')
		else:
			raise Exception('Referenced dataset should contain "x" and "y" columns')
	
	# Gives a prediction
	def query(self, data, return_ensembled=False):
		ret = []
		for engine in self.engines:
			ret.append(True if engine.predict([data])[0] > 0.5 else False)

		if return_ensembled == True:
			return ret
		else:
			# checks if True predictors are more than False ones
			return True if sum(ret) > len(ret) - sum(ret) else False


if __name__=='__main__':
	api = API()

	# Initialize the engine anew; train the tokenizer on a file labled.csv
	api.connect(engine_type='NTVNB', optional={'corpora': ['../data/labeled.csv']})

	# Train the engine
	api.train('../data/labeled.csv')
	print(api.query('Hello world kvartira'))

	# Dump the engine into a given file
	api.dump_engine('../engine_dumps/NTVNB.pkl')

	# Dataset manipulation
	print(api.dataset_stats('../data/labeled.csv'))
	api.dataset_update([['hello', 0]], '../data/labeled.csv')
	print(api.dataset_stats('../data/labeled.csv'))

	# Load the engine from a file
	api.connect(engine_path='../engine_dumps/NTVNB.pkl')
	print(api.query('Hello world kvartira'))
