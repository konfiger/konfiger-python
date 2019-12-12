
'''
	The MIT License
	
	Copyright 2019 Adewale Azeez <azeezadewale98@gmail.com>.
'''

'''

'''
class KeyValueObject:

	'''
	
	'''
	def __init__(self, key, value):
		if not isinstance(key, str) or not isinstance(value, str):
			raise AttributeError("com.azeezadewale.KeyValueObject: Invalid parameter expecting string as key and value")
		self.key = key.strip()
		self.value = value

	'''
	
	'''
	def get_key(self):
		return self.key

	'''
	
	'''
	def get_value(self):
		return self.value

	'''
	
	'''
	def set_key(self, key):
		self.key = key.strip()

	'''
	
	'''
	def set_value(self, value):
		self.value = value

	'''
	
	'''
	def __str__(self):
		return "<KeyValueObject@" + str(hash(self.key * 1000)) + ":Key=" + self.key + ",Value=" + self.value + ">";
		
		