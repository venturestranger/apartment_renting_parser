class NTVNB_Config:
	ALPHABET = '0123456789+qwertyuiopasdfghjklzxcvbnm '
	MAX_TOKEN_LENGTH = 2
	VOCAB_SIZE = 1500
	LATINIZE_CORPORA = True

class RNN_Config:
	ALPHABET = '0123456789+qwertyuiopasdfghjklzxcvbnm '
	MAX_TOKEN_LENGTH = 2
	VOCAB_SIZE = 1500
	SENTENCE_SIZE = 100

class KWC_Config:
	ADDS = ['ищ', 'сня', 'сним', 'кварт', 'аренд', 'дом', 'куп', 'недвиж', 'съем', 'догов', 'плат', 'бюдж', 'срок', 'жиль', 'прож', 'врем', 'час', 'житл', 'терм', 'оренд', 'нерухо', 'будин', 'шук', 'kir', 'ev', 'dai', 'kon', 'geç', 'sür', 'ödem', 'gayrime']
	SUBS = ['сда']
	THRESHOLD = 2

class Config:
	engine_configs = {
		'NTVNB': NTVNB_Config,
		'RNN': RNN_Config,
		'KWC': KWC_Config
	}
