
'''
	The MIT License
	
	Copyright 2019 Adewale Azeez <azeezadewale98@gmail.com>.
'''

from key_value_db.key_value_object import KeyValueObject

'''

'''
class KeyValueDB:

	'''
	
	'''
	def __init__(self, key_value_text="", case_sensitive=True, delimeter='=', seperator='\n', err_tolerance=False):
		self.db_changed = True
		self.__string_value = ""
		self.key_value_objects = []
		self.iterator_index = 0;
		
		self.key_value_text = key_value_text
		self.case_sensitive = case_sensitive
		self.delimeter = delimeter
		self.seperator = seperator
		self.err_tolerance = err_tolerance
		self.__parse(key_value_text, case_sensitive, delimeter, seperator, err_tolerance)
		
	'''
	
	'''
	def __iter__(self):
		return self
		
	'''
	
	'''
	def __next__(self):
		if self.iterator_index > len(self.key_value_objects) - 1:
			raise StopIteration
		else:
			self.iterator_index += 1
			return self.key_value_objects[self.iterator_index - 1]
		
	'''
	
	'''
	def next(self):
		if self.iterator_index > len(self.key_value_objects) - 1 :
			raise StopIteration
		else:
			self.iterator_index += 1
			return self.key_value_objects[self.iterator_index - 1]
			
	'''
	
	'''
	def __getitem__(self, index):
		if index >= len(self.key_value_objects):
			raise IndexError("com.azeezadewale.KeyValueDB: CustomRange index out of range " + str(index))
		return self.key_value_objects[index]
		
	'''
	
	'''
	def __len__(self):
		return len(self.key_value_objects)
		
	'''
	
	'''
	def get_key_value_object(self, index_key, default_key_value_object=KeyValueObject("", "")):
		if isinstance(index_key, int):
			return self.key_value_objects[index_key]
			
		elif isinstance(index_key, str):
			index_key = (index_key.lower() if not self.case_sensitive else index_key)
			for key_value_object in self.key_value_objects:
				if key_value_object.get_key() == index_key:
					return key_value_object
			return default_key_value_object
		else:
			raise TypeError("com.azeezadewale.KeyValueDB.get_keyValueObject: Invalid parameter expecting string or number")
		
	'''
	
	'''
	def get_like_key_value_object(self, key, default_key_value_object=KeyValueObject("", "")):
		if isinstance(key, str):
			key = (key.lower() if not self.case_sensitive else key)
			for key_value_object in self.key_value_objects:
				if key in key_value_object.get_key():
					return key_value_object
			return default_key_value_object
		else:
			raise TypeError("com.azeezadewale.KeyValueDB.getLikeKeyValueObject: Invalid parameter expecting string")
		
	'''
	
	'''
	def get(self, index_key, default_value=""):
		if isinstance(index_key, int):
			return self.key_value_objects[index_key].get_value()
			
		elif isinstance(index_key, str):
			index_key = (index_key.lower() if not self.case_sensitive else index_key)
			for key_value_object in self.key_value_objects:
				if key_value_object.get_key() == index_key:
					return key_value_object.get_value()
			if isinstance(default_value, str):
				return default_value
			elif isinstance(default_value, KeyValueObject):
				return default_value.get_value()
			else:
				raise TypeError("com.azeezadewale.KeyValueDB.get: Invalid second parameter expecting string or KeyValueObject")
			
		else:
			raise TypeError("com.azeezadewale.KeyValueDB.get: Invalid parameter expecting string or number")
		
	'''
	
	'''
	def get_like(self, key, default_value=""):
		if isinstance(key, str):
			key = (key.lower() if not self.case_sensitive else key)
			for key_value_object in self.key_value_objects:
				if key in key_value_object.get_key():
					return key_value_object.get_value()
			if isinstance(default_value, str):
				return default_value
			elif isinstance(default_value, KeyValueObject):
				return default_value.get_value()
			else:
				raise TypeError("com.azeezadewale.KeyValueDB.get: Invalid second parameter expecting string or KeyValueObject")
		else:
			raise TypeError("com.azeezadewale.KeyValueDB.getLikeKeyValueObject: Invalid parameter expecting string")
			
	'''
	
	'''
	def set(self, index_key, value):
		if not isinstance(value, str):
			raise TypeError("com.azeezadewale.KeyValueDB.set: Invalid second parameter expecting string")
			
		if isinstance(index_key, int):
			self.key_value_objects[index_key].set_value(value)
			self.db_changed = True
			
		elif isinstance(index_key, str):
			index_key = (index_key.lower() if not self.case_sensitive else index_key)
			for key_value_object in self.key_value_objects:
				if key_value_object.get_key() == index_key:
					key_value_object.set_value(value)
					self.db_changed = True
					return
			self.add(index_key, value)
			
		else:
			raise TypeError("com.azeezadewale.KeyValueDB.set: Invalid parameter expecting string or number")
			
	'''
	
	'''
	def set_key_value_object(self, index_key, key_value_object_value):
		if not isinstance(key_value_object_value, KeyValueObject):
			raise TypeError("com.azeezadewale.KeyValueDB.set_keyValueObject: Invalid second parameter expecting KeyValueObject")
			
		if isinstance(index_key, int):
			self.key_value_objects[index_key] = key_value_object_value
			self.db_changed = True
			
		elif isinstance(index_key, str):
			index_key = (index_key.lower() if not self.case_sensitive else index_key)
			for i in range(0, len(self.key_value_objects)):
				if self.key_value_objects[i].get_key() == index_key:
					self.key_value_objects[i] = key_value_object_value
					self.db_changed = True
					return 
			self.add(key_value_object_value)
			
		else:
			raise TypeError("com.azeezadewale.KeyValueDB.set_keyValueObject: Invalid parameter expecting string or number")
			
	'''
	
	'''
	def add(self, key_value_object_value_key, value=""):
		if isinstance(key_value_object_value_key, KeyValueObject):
			if not isinstance(value, str):
				raise TypeError("com.azeezadewale.KeyValueDB.add: Only one parameter is expecter when adding a KeyValueObject")
			if value != "":
				raise TypeError("com.azeezadewale.KeyValueDB.add: Only one parameter is expecter when adding a KeyValueObject")
			
			if self.get((key_value_object_value_key.get_key().lower() if not self.case_sensitive else key_value_object_value_key.get_key())) != "":
				self.set_keyValueObject((key_value_object_value_key.get_key().lower() if not self.case_sensitive else key_value_object_value_key.get_key()), key_value_object_value_key)
				return
			self.key_value_objects.append(key_value_object_value_key)
			self.db_changed = True
			
		elif isinstance(key_value_object_value_key, str):
			key_value_object_value_key = (key_value_object_value_key.lower() if not self.case_sensitive else key_value_object_value_key)
			if self.get(key_value_object_value_key) != "":
				self.set(key_value_object_value_key, value)
				return
			self.key_value_objects.append(KeyValueObject(key_value_object_value_key, value))
			self.db_changed = True
			
		else:
			raise TypeError("com.azeezadewale.KeyValueDB.add: Invalid first parameter expecting string or KeyValueObject")
			
	'''
	
	'''
	def remove(self, index_key):
		if isinstance(index_key, int):
			ret_key_value_object = self.key_value_objects[index_key]
			del self.key_value_objects[index_key]
			self.db_changed = True
			return ret_key_value_object
			
		elif isinstance(index_key, str):
			ret_key_value_object = KeyValueObject("", "")
			index_key = (index_key.lower() if not self.case_sensitive else index_key)
			for i in range(0, len(self.key_value_objects)):
				if self.key_value_objects[i].get_key() == index_key:
					ret_key_value_object = self.key_value_objects[i]
					del self.key_value_objects[i]
					self.db_changed = True
					break 
			return ret_key_value_object
			
		else:
			raise TypeError("com.azeezadewale.KeyValueDB.remove: Invalid parameter expecting string or number")
		
		
	'''

	'''
	def __parse(self, key_value_text="", case_sensitive=True, delimeter='=', seperator='\n', err_tolerance=False):
		characters = list(key_value_text.replace('\r', ''))
		key = ""
		value = ""
		parse_key = True
		line = 1
		column = 0
		
		for i in range(0, len(characters)):
			if i == len(characters) - 1: 
				if key != "":
					if key == "" and value == "": 
						continue 
					if parse_key and not err_tolerance:
						raise AttributeError("com.azeezadewale.KeyValueDB: Invalid entry detected near Line " + str(line) + ":" + str(column))
					self.key_value_objects.append(KeyValueObject(key, value))
				break
				
			character = characters[i]
			
			column = column + 1
			if character == "\n":
				line = line + 1
				column = 0
				
			if character == seperator:
				if key == "" and value == "":
					continue 
				if parse_key and not err_tolerance:
					raise AttributeError("com.azeezadewale.KeyValueDB: Invalid entry detected near Line " + str(line) + ":" + str(column))
				self.key_value_objects.append(KeyValueObject(key, value))
				parse_key = True
				key = ""
				value = ""
				continue
			
			if character == delimeter:
				if value != "" and not err_tolerance:
					raise AttributeError("com.azeezadewale.KeyValueDB: The input is imporperly sepreated near Line " + str(line) + ":" + str(column) +". Check the seperator")
				parse_key = False
				continue
				
			if parse_key:
				key += (character.lower() if not case_sensitive else character)
			else:
				value += character

	'''
	
	'''
	def __str__(self):
		if self.db_changed:
			self.__string_value = ""
			for i in range(0, len(self.key_value_objects)):
				self.__string_value += self.key_value_objects[i].get_key() + self.delimeter + self.key_value_objects[i].get_value()
				if i != len(self.key_value_objects) - 1:
					self.__string_value += self.seperator
			self.db_changed = False
		return self.__string_value

	'''
	
	'''
	def clear(self):
		self.key_value_objects = []

	'''
	
	'''
	def is_empty(self):
		return len(self.key_value_objects) == 0

	'''
	
	'''
	def size(self):
		return len(self.key_value_objects)
		