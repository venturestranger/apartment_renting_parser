# API Backend (venturestranger)

## Introduction
This backend implements an API class that provides functionality for initializing, dumping, and training engines, as well as processing data for predictions.

## API Class

```python
api = API()
```

### Methods

1. **`.connect(engine_type='NTVNB', engine_types=[], engine_path=None, optional={})`**
   - Initializes an engine for the API.
   - `engine_type: str` - Type of engine to initialize if an existing engine is not specified. Currently, only the `NTVNB` engine is available.
   - `engine_path: str` - Path to an existing engine.
   - `optional: dict` - Additional parameters for engines to initialize (`'corpora'` with a list of document paths for an NTVNB tokenizer to train).
   - `engine_types: list` - A list of engines to enable ensembling.

```python
api.connect(engine_type='NTVNB', optional={'corpora': ['./data/raw.csv']})
```

```python
api.connect(engine_type='KWC'})
```

```python
api.connect(engine_types=['NTVNB', 'KWC', 'NTVRF'], optional={'corpora': ['./data/raw.csv']})
```

```python
api.connect(engine_path='./data/engine_dumps/model1.pkl')
```

2. **`.dump_engine(engine_path)`**
   - Dumps an API engine to a specified file.
   - `engine_path: str` - Path to a `.pkl` file where the engine will be dumped.

```python
api.dump_engine('./engine_dumps/model1.pkl')
```

3. **`.dataset_stats(dataset_path)`**
   - Fetches statistics of a dataset: a number of positive and negative labels.
   - `dataset_path: str` - Path to a dataset to get stats.

```python
stats = api.dataset_stats('./data/labeled.csv')
print(stats['pos'], stats['neg'])
```

4. **`.dataset_update(data_points, dataset_path)`**
   - Updates a dataset with new data points.
   - `data_points: list[list(2)]` - A list of new data points consisting of two variables (str, float) respective to (x, y) columns in the dataset.
   - `dataset_path: str` - Path to a dataset to update.

```python
api.dataset_update([['Сдам квартиру', 0], ['Арендую квартиру', 1]], './data/labeled.csv')
```

5. **`.train(dataset_path, portion=1.)`**
   - Fits an API engine on a dataset.
   - `dataset_path: str` - Path to a dataset to train the engine on.
   - `portion` - Indicates a fraction of the specified dataset to train the engine on.

```python
api.train('./data/labeled.csv')
```

6. **`.query(data)`**
   - Processes a string and returns a prediction.
   - `data: str` - A string to process.

```python
prediction = api.query('Сниму квартиру в марте')
```

## Engines

1. **KWC (Non-trainable)** - Key Words Classifier
   - Calculates the number of positively-key words found in the text and subtracts the number of negatively-key words. The prediction is true if the difference is more than the set threshold. The engine uses the Aho-Corasick algorithm to quickly check matchings.

2. **NTVNB (Trainable)** - Naive Bayes Classifier with Text Normalization, Tokenization, and Words Bagging
   - Normalizes the text, tokenizes it, and returns the bag of words. The bag of words is then classified by a Naive Bayes classifier.
   - Requires `optional` argument when connecting. `opitonal` argument should contain `corpora` key with a path to corpora to train tokenizer.

3. **NTVRF (Trainable)** - Random Forest Classifier with Text Normalization, Tokenization, and Words Bagging
   - Normalizes the text, tokenizes it, and returns the bag of words. The bag of words is then classified by a Random Forest classifier.
   - Requires `optional` argument when connecting. `opitonal` argument should contain `corpora` key with a path to corpora to train tokenizer.
