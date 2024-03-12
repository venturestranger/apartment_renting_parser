class NTVNB_Config:
	ALPHABET = '0123456789+qwertyuiopasdfghjklzxcvbnm '
	MAX_TOKEN_LENGTH = 4
	VOCAB_SIZE = 2000

class Config:
	engine_configs = {
		'NTVNB': NTVNB_Config
	}
