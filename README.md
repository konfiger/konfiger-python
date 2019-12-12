# <p style="text-align: center;" align="center"><img src="https://github.com/keyvaluedb/key-value-db/raw/master/icons/key-value-db-python.png" alt="key-value-db-python" style="width:180px;height:160px;" width="180" height="160" /><br /> key-value-db-python</p>

<p style="text-align: center;" align="center">Light weight package to quickly and easily manage, load, update and save key-value type database </p>

The sample use cases of this package is loading configuration file, language file, preference setting in an application. More use cases can be seen [here](https://keyvaluedb.github.io/usecases/index.html).

The package does not do any Input and Output operation as there are several way to read and write to file and the methods has their strength and weakness therefore the developer has to find the efficient way to load and save locally.

___

## Table of content
- [Installation](#installation)
- [Example](#example)
- [Legends](#legends)
- [API](#api)
	- [Creating/loading a document](#creating/loading-a-document)
	- [Inserting data](#inserting-data)
	- [Finding data](#finding-data)
	    - [Get KeyValue Object](#get-keyvalue-object)
	    - [Get Like KeyValue Object](#get-like-keyvalue-object)
	    - [Get](#get-like)
	    - [Get Like](#get-like)
	- [Updating data](#updating-data)
        - [Set](#set)
        - [Set KeyValue Object](#set-keyvalue-object)
	- [Inserting data](#inserting-data)
	- [Removing data](#removing-data)
	- [Size, Clear, isEmpty](#size,-clear,-isempty)
        - [Size](#size)
        - [Clear](#clear)
        - [isEmpty](#isempty)
    - [Saving collection](#saving-collection)
    - [Iterating collection](#iterating-collection)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)

## Installation

Install the package from the Python package index or download the zip and .egg file from [releases](https://github.com/keyvaluedb/key-value-db-java/releases).

```bash
pip install key_value_db
```

## Example

The following example load, update, read and remove a simple key value object 

```python
from key_value_db import KeyValueDB, KeyValueObject

#initialize the key-value
key_value_db = KeyValueDB("Greet=Hello World,Project=KeyValueDB", True, '=', ',', False)

#get an object
print(key_value_db.get("Greet"))

#remove an object
key_value_db.remove("Greet")

#add an object
key_value_db.add("What", "i don't know what to write here")

#print all the objects
for kvo in key_value_db:
	print(kvo)
```

## Legends

```
kvp  - Key Value Pair
kvdb - Key value Database
pss  - Possibly
kvo  - Key Value Object
```

## API

Only string type is used as the key and value of the kvo. A kvo can be used to replace or set the value for a key.

### Creating/loading a document

You can use the package to update and create an existing key value database. This library does not read the database from a file which means you have to find a way to read a string from the file. 

Create a new keyValueDB. The default seperator between the key and value is `=` and the delimeter between the kvp is `\n`(newline).

```python
key_value_db = KeyValueDB()
```

To load existing KeyValueDB  

```python
key_value_db = KeyValueDB(
        "Greet=Hello World,Project=KeyValueDB", #pss read string from file
        True, #case sensitive is true
        '=', #the seperator from key and value
        ',', #the delimeter for the key-value-pair
        False #error tolerance if true no exception is thrown
        )
```

### Inserting Data

The only accepted type that can be inserted is a valid `KeyValueObject` and `String`. The method `add` can be used to add a new kvp into the object.

Add a kvp with it key and value

```python
key_value_db.add("Greet", "Hello World");
```

Add a kvp using the `KeyValueObject` class.

```python
key_value_object = KeyValueObject("Greet", "Hello World");
key_value_db.add(keyValueObject);
```

### Finding Data

There are several way to find and get a value from the kvdb object. The value or the KeyValueObject can be gotten using the methods below

#### Get KeyValue Object

You can get the kvo using either the key or index. If the corresponding kvo is not found, an empty kvo is added to the db and then returned but not in the case when requested with the integer index. If a fallback kvo is sent as second parameter then when the request kvo is not found the fallback second parameter is added to the kvdb and then returned.

Get the kvo using it integer index

```python
key_value_db.getKeyValueObject(0);
//dev.sourcerersproject.KeyValueObject@4554617c:Key=Greet,Value=Hello World
```

Get the kvo using it key 

```python
keyValueDB.getKeyValueObject("Greet");
//dev.sourcerersproject.KeyValueObject@4554617c:Key=Greet,Value=Hello World
```

Get the kvo using it key with fallback kvo

```python
final KeyValueObject keyValueObject = new KeyValueObject("Name", "Adewale Azeez");
keyValueDB.getKeyValueObject("Name", keyValueObject);
//KeyValueObject {hashcode: 765363576, key: "Name", value: "Adewale Azeez"}
```

#### Get Like KeyValue Object

Get a kvo by checking the kvdb for the kvo object that contains a part of the key. If a fallback kvo is sent as second parameter then when the request kvo is not found the fallback second parameter is added to the kvdb and then returned.

Get a similar kvo using it key part 

```python
keyValueDB.getLikeKeyValueObject("eet");
//dev.sourcerersproject.KeyValueObject@4554617c:Key=Greet,Value=Hello World
```

Get a similar kvo using it key part with fallback kvo

```python
final KeyValueObject keyValueObject = new KeyValueObject("Name", "Adewale Azeez");
keyValueDB.getKeyValueObject("Nam", keyValueObject);
//dev.sourcerersproject.KeyValueObject@4554617c:Key=Name,Value=Adewale Azeez
```

#### Get

You can get a kvdb value using either the key or index. If the corresponding value is not found, an empty string is added to the db and then returned but not in the case when requested with the integer index. 

If a fallback kvo is sent as second parameter then when the request key is not found the fallback second parameter is added to the kvdb and then value is returned. If a string value is sent as the second value it is returned if the key is not found in the kvdb.

Get a value using it integer index

```python
keyValueDB.get(0);
//"Hello World"
```

Get the value using it key 

```python
keyValueDB.get("Greet");
//"Hello World"
```

Get the kvo using it key with fallback value

```python
keyValueDB.get("Licence", "The MIT Licence");
//"The MIT Licence"
```

Get the kvo using it key with fallback kvo

```python
final KeyValueObject keyValueObject = new KeyValueObject("Licence", "The MIT Licence");
keyValueDB.get("Name", keyValueObject);
//"The MIT Licence"
```

#### Get Like 

Get a value by checking the kvdb for the kvo object that contains a part of the key. 

If a fallback kvo is sent as second parameter then when the request key is not found the fallback second parameter is added to the kvdb and then value is returned.

Get a value using it key part 

```python
keyValueDB.getLike("eet");
//"Hello World"
```

Get a value using it key part with fallback kvo

```python
final KeyValueObject keyValueObject = new KeyValueObject("Licence", "The MIT Licence");
keyValueDB.getLike("Li", keyValueObject);
//"The MIT Licence"
```

### Updating Data

There are various way to update a kvp in the kvdb, the value can be changed directly or set to a new KeyValueObject. If you try to set a kvo that does not exist in the kvdb using it key, it is added to the kvdb.

#### Set

The `set` method is used to change the value of the kvo using the index of the kvo or a kvo key. 

Set a kvo value using it index

```python
keyValueDB.set(0, "Hello World from thecarisma");
//dev.sourcerersproject.KeyValueObject@4554617c:Key=Greet,Value=Hello World from thecarisma
```

Set a kvo value using it key

```python
keyValueDB.set("Greet", "Hello World from thecarisma");
//dev.sourcerersproject.KeyValueObject@4554617c:Key=Greet,Value=Hello World from thecarisma
```

#### Set KeyValue Object

Completly change a KeyValueObject in the kvdb using either it index or it key. The kvo is completly replaced which means unique fields like the hashcode of the kvo changes. When the kvo is set using it key if the corresponding kvo does not exist it is added into the kvdb.
Note that this method completly changes the kvo so it can be used to replace a kvo.

Set a kvo using it index

```python
final KeyValueObject keyValueObject = new KeyValueObject("Licence", "The MIT Licence");
keyValueDB.setKeyValueObject(0, keyValueObject);
//dev.sourcerersproject.KeyValueObject@4554617c:Key=Licence,Value=The MIT Licence
```

Set a kvo value using it key

```python
final KeyValueObject keyValueObject = new KeyValueObject("Licence", "The MIT Licence");
keyValueDB.setKeyValueObject("Greet", keyValueObject);
//dev.sourcerersproject.KeyValueObject@4554617c:Key=Licence,Value=The MIT Licence
```

### Inserting Data

A new kvp can be inserted by invoking the `add` method. The kvp can be added using it key and value or by directly adding the KeyValueObject to the kvdb. 

Add a new kvp using the key and value

```python
keyValueDB.add("Key", "This is the value");
```

Add a new kvp using a new KeyValueObject

```python
final KeyValueObject keyValueObject = new KeyValueObject("Key", "This is the value");
keyValueDB.add(keyValueObject);
```

### Removing Data

Remove a kvp completely from the kvdb using either it key of the integer index. The kvp that was removed is returned from the method. If the index does not exist out of bound error occur and if a kvo with the key is not present nothing is done but an empty kvo is returned.

Remove a kvp using integer index

```python
keyValueDB.remove(0);
//removes the first kvp in the kvdb
//dev.sourcerersproject.KeyValueObject@4554617c:Key=Greet,Value=Hello World
```

Remove a kvp using it key

```python
keyValueDB.remove("Greet");
//removes the first kvp in the kvdb
//dev.sourcerersproject.KeyValueObject@4554617c:Key=Greet,Value=Hello World
```

## Size, Clear, isEmpty

### Size

Get the size of the kvo in the kvdb.

```python
keyValueDB.size();
//4
```

### Clear

Remove all the elements and kvo from the kvdb

```python
keyValueDB.clear();
//keyValueDB.size() = 0
```

### isEmpty

Check whether the kvdb contains any kvo in it.

```python
keyValueDB.isEmpty();
//false
```

## Saving collection

The kvp collection kvdb can be inspected as a string using the `toString` method. The returned value can be saved locally by writing to a persistent storage or to a plain text file. The output of the `toString` method is determined by the kvos, the seperator and the delimeter.

```python
keyValueDB.toString();
// "Greet=Hello World,Project=KeyValueDB,Project=KeyValueDB,Licence=The MIT Licence"
```

## Iterating collection

The KeyValueDB object can be iterated natively using the `for..of` loop expression. 

```python
for (KeyValueObject KeyValueObject : keyValueDB) {
    //operate on the KeyValueObject
}
```

## Contributing

Before you begin contribution please read the contribution guide at [CONTRIBUTING GUIDE](https://keyvaluedb.github.io/contributing.html)

You can open issue or file a request that only address problems in this implementation on this repo, if the issue address the concepts of the package then create an issue or rfc [here](https://github.com/keyvaluedb/key-value-db/)

## Support

You can support some of this community as they make big impact in the developement of people to get started with software engineering and open source.

- https://www.patreon.com/devcareer
- https://opencollective.com/osca

Or you can support me to continue making awesome open source projects > https://patreon.com/thecarisma. Thanks!🤗

**You can make big difference**.

## License

MIT License Copyright (c) 2019 Adewale Azeez - keyvaluedb

