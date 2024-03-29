import pandas as pd
import pickle
from .config import Config
from .engines import NTVRF
from .engines import NTVNB
from .engines import KWC
from sklearn.model_selection import train_test_split


# Implements an API interface
class API:
	def __init__(self):
		pass

	# Initializes a new engine (predicting model) or loads one from <engine_dir>
	def connect(self, engine_type='NTVRF', engine_types=[], engine_path=None, optional={}):
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
					case 'NTVRF':
						self.engines.append(NTVRF(Config.engine_configs[engine], optional['corpora']))
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
	def train(self, dataset_path, portion=1.):
		df = pd.read_csv(dataset_path)

		if 'x' in df.columns and 'y' in df.columns:
			for engine in self.engines:
				try:
					x, x_, y, y_ = train_test_split(df['x'], df['y'], test_size=1.-portion, stratify=df['y'])
					engine.fit(x, y)
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
