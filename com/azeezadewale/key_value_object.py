
'''
	The LGPL-3.0 License
	
	Copyright 2019 Azeez Adewale <azeezadewale98@gmail.com>.
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
	def getKey(self):
		return self.key

	'''
	
	'''
	def getValue(self):
		return self.value

	'''
	
	'''
	def setKey(self, key):
		self.key = key.strip()

	'''
	
	'''
	def setValue(self, value):
		self.value = value

	'''
	
	'''
	def __str__(self):
		return "<KeyValueObject@" + str(hash(self.key * 1000)) + ":Key=" + self.key + ",Value=" + self.value + ">";
		
		