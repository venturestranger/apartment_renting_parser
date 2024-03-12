# Description
A collaborative project for implicit house renting requests recognition

1. Client - Telebot + Telethon
2. Backend - Scikit-learn + HuggingFace Tokenizer

# Backend (venturestranger)
Implements an API class

### Methods:
1. `.connect(engine_type='NTVNB', engine_path=None, optional={})` - initializes an engine for API
   * `engine_type: str` - type of engine to initialize if an existing engine not specified
   * `engine_path: str` - a path to an existing engine
   * `optional: dict` - additional parameters for engines to initialize ('corpora' with a list of document paths for a NTVNB tokenizer to train)

2. `.dump_engine(engine_path)` - dumps an API engine
   * `engine_path: str` - a path to a .pkl file where to dump the engine
  
3. `.dataset_stats(dataset_path)` - fetches stats of a dataset
   * `dataset_path: str` - a path to a dataset to get stats
  
4. `.dataset_update(data_points, dataset_path)` - updates a dataset with new data points
   * `data_points: list[list(2)]` - a list of new data points consisting of two variables (str, float) respective to (x, y) columns in the dataset
   * `dataset_path: str` - a path to a dataset to update
  
5. `.train(dataset_path)` - fits an API engine on a dataset
   * `dataset_path: str` - a path to a dataset to train the engine on
  
6. `.query(data)` - processes a string and gives a prediction
   * `data: str` - a string to process

# Client

