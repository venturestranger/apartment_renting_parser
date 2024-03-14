class NTVNB_Config:
	ALPHABET = '0123456789+qwertyuiopasdfghjklzxcvbnm '
	MAX_TOKEN_LENGTH = 4
	VOCAB_SIZE = 5000

class KWC_Config:
	SUBS = ['ищ', 'сним', 'кварт', 'аренд', 'дом', 'куп', 'недвиж', 'съем', 'догов', 'плат', 'бюдж', 'срок', 'жиль', 'прож', 'врем', 'час', 'житл', 'терм', 'оренд', 'нерухо', 'будин', 'шук', 'kir', 'ev', 'dai', 'kon', 'geç', 'sür', 'ödem', 'gayrime']
	THRESHOLD = 2

class Config:
	engine_configs = {
		'NTVNB': NTVNB_Config,
		'KWC': KWC_Config
	}
