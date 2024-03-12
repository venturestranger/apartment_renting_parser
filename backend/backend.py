from config import Config
import pandas as pd
import pickle
from engines import NTVNB

# Implements an API interface
class API:
	def __init__(self):
		pass

	# Initializes a new engine (predicting model) or loads one from <engine_dir>
	def connect(self, engine_type='NTVNB', engine_path=None, optional={}):
		if engine_path != None:
			try:
				with open(engine_path, 'rb') as f:
					self.engine = pickle.load(f)
			except:
				raise Exception('Error while loading the engine')
		else:
			if engine_type == 'NTVNB':
				self.engine = NTVNB(Config.engine_configs[engine_type], optional['corpora'])
			else:
				raise Exception('No such engine exists')
	
	# Dumps the used engine
	def dump_engine(self, engine_path=None):
		try:
			with open(engine_path, 'wb') as f:
				pickle.dump(self.engine, f)
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
			raise Exception('Rows in the provided data should have only two values for "x" and "y" columns')
		else:
			df.to_csv(dataset_path)

	# Retrains the engine on a given dataset
	def train(self, dataset_path):
		df = pd.read_csv(dataset_path)

		try:
			self.engine.fit(df['x'], df['y'])
		except:
			raise Exception('Referenced dataset should contain "x" and "y" columns')
	
	# Gives a prediction
	def query(self, data):
		return True if self.engine.predict([data])[0] > 0.5 else False


if __name__=='__main__':
	api = API()

	# Initialize the engine anew
	api.connect(engine_type='NTVNB', optional={'corpora': ['./data/raw.csv']})

	# Train the engine
	api.train('./data/labled.csv')

	# Dump the engine into a given file
	api.dump_engine('./engine_dumps/NTVNB.pkl')

	# Dataset manipulation
	print(api.dataset_stats('./data/labled.csv'))
	print(api.query('Hello world kvartira'))
	api.dataset_update([['hello', 0]], './data/labled.csv')
	print(api.dataset_stats('./data/labled.csv'))

	# Load the engine from a file
	api.connect(engine_path='./engine_dumps/NTVNB.pkl')
	print(api.query('Hello world kvartira'))
