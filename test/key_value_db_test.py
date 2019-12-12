
from key_value_db import KeyValueDB, KeyValueObject

key_value_DB = KeyValueDB("One=Adewale\nThrees=3333", True, '=', '\n', False)
for kvo in key_value_DB:
	print(kvo)
	
print()
        
print(key_value_DB.get("Greeting"))
key_value_DB.set("Greeting", "Hello from Adewale Azeez")
key_value_DB.add("One", "Added another one element")
key_value_DB.add("Null", "Remove this")
print(key_value_DB.get_like("Three"))

print()
for kvo in key_value_DB:
	print(kvo)

print()
print("Removed: " + str(key_value_DB.remove("Null")))

print(key_value_DB)
print()
key_value_DB.add("Two", "Added another two element")
print(key_value_DB)
print()
key_value_DB.add("Three", "Added another three element")
print(key_value_DB)
print()
print(key_value_DB.size())
print(key_value_DB.is_empty())
print(key_value_DB.clear())
print(key_value_DB.size())
print(key_value_DB.is_empty())
print()