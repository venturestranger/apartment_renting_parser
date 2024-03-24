from backend.backend import API

api = API()

# initialize an engine from a file 
api.connect(engine_path='./engine_dumps/KWC_NTVNB.pkl')

# Train the engine
print(api.query('квартира дом жилье'))
