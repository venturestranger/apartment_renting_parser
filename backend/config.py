class NTVNB_Config:
	ALPHABET = '0123456789+qwertyuiopasdfghjklzxcvbnm '
	MAX_TOKEN_LENGTH = 2
	VOCAB_SIZE = 1500
	LATINIZE_CORPORA = True

class NTVRF_Config:
	ALPHABET = '0123456789+qwertyuiopasdfghjklzxcvbnm '
	MAX_TOKEN_LENGTH = 5
	VOCAB_SIZE = 4000
	LATINIZE_CORPORA = True
	N_ESTIMATORS = 150
	MAX_DEPTH = 15

class RNN_Config:
	ALPHABET = '0123456789+qwertyuiopasdfghjklzxcvbnm '
	MAX_TOKEN_LENGTH = 2
	VOCAB_SIZE = 1500
	MAX_TOKENS = 200

class KWC_Config:
	ADDS = ['ищ', 'сня', 'сним', 'кварт', 'аренд', 'дом', 'куп', 'недвиж', 'съем', 'догов', 'плат', 'бюдж', 'срок', 'жиль', 'прож', 'врем', 'час', 'житл', 'терм', 'оренд', 'нерухо', 'будин', 'шук', 'kir', 'ev', 'dai', 'kon', 'geç', 'sür', 'ödem', 'gayrime', 'куп', 'прод', 'апар']
	SUBS = []
	THRESHOLD = 2

class Config:
	engine_configs = {
		'NTVRF': NTVRF_Config,
		'NTVNB': NTVNB_Config,
		'KWC': KWC_Config
	}
