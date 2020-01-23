

Light weight package to quickly and easily manage, load, update and save
key-value type database

The sample use cases of this package is loading configuration file,
language file, preference setting in an application. More use cases can
be seen `here <https://keyvaluedb.github.io/usecases/index.html>`__.

The package does not do any Input and Output operation as there are
several way to read and write to file and the methods has their strength
and weakness therefore the developer has to find the efficient way to
load and save locally.

--------------

Table of content
----------------

-  `Installation <#installation>`__
-  `Example <#example>`__
-  `Legends <#legends>`__
-  `API <#api>`__

   -  `Creating/loading a document <#creating/loading-a-document>`__
   -  `Inserting data <#inserting-data>`__
   -  `Finding data <#finding-data>`__

      -  `Get KeyValue Object <#get-keyvalue-object>`__
      -  `Get Like KeyValue Object <#get-like-keyvalue-object>`__
      -  `Get <#get-like>`__
      -  `Get Like <#get-like>`__

   -  `Updating data <#updating-data>`__

      -  `Set <#set>`__
      -  `Set KeyValue Object <#set-keyvalue-object>`__

   -  `Inserting data <#inserting-data>`__
   -  `Removing data <#removing-data>`__
   -  `Size, Clear, isEmpty <#size,-clear,-isempty>`__

      -  `Size <#size>`__
      -  `Clear <#clear>`__
      -  `isEmpty <#isempty>`__

   -  `Saving collection <#saving-collection>`__
   -  `Iterating collection <#iterating-collection>`__

-  `How it works <#how-it-works>`__
-  `Contributing <#contributing>`__
-  `Support <#support>`__
-  `License <#license>`__

Installation
------------

Install the package from the Python package index or download the zip
and .egg file from
`releases <https://github.com/keyvaluedb/key-value-db-python/releases>`__.

.. code:: bash

    pip install key_value_db

Example
-------

The following example load, update, read and remove a simple key value
object

.. code:: python

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

Legends
-------

::

    kvp  - Key Value Pair
    kvdb - Key value Database
    pss  - Possibly
    kvo  - Key Value Object

API
---

Only string type is used as the key and value of the kvo. A kvo can be
used to replace or set the value for a key.

Creating/loading a document
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the package to update and create an existing key value
database. This library does not read the database from a file which
means you have to find a way to read a string from the file.

Create a new keyValueDB. The default seperator between the key and value
is ``=`` and the delimeter between the kvp is ``\n``\ (newline).

.. code:: python

    key_value_db = KeyValueDB()

To load existing KeyValueDB

.. code:: python

    key_value_db = KeyValueDB(
            "Greet=Hello World,Project=KeyValueDB", #pss read string from file
            True, #case sensitive is true
            '=', #the seperator from key and value
            ',', #the delimeter for the key-value-pair
            False #error tolerance if true no exception is thrown
            )

Inserting Data
~~~~~~~~~~~~~~

The only accepted type that can be inserted is a valid
``KeyValueObject`` and ``String``. The method ``add`` can be used to add
a new kvp into the object.

Add a kvp with it key and value

.. code:: python

    key_value_db.add("Greet", "Hello World")

Add a kvp using the ``KeyValueObject`` class.

.. code:: python

    key_value_object = KeyValueObject("Greet", "Hello World")
    key_value_db.add(keyValueObject)

Finding Data
~~~~~~~~~~~~

There are several way to find and get a value from the kvdb object. The
value or the KeyValueObject can be gotten using the methods below

Get KeyValue Object
^^^^^^^^^^^^^^^^^^^

You can get the kvo using either the key or index. If the corresponding
kvo is not found, an empty kvo is added to the db and then returned but
not in the case when requested with the integer index. If a fallback kvo
is sent as second parameter then when the request kvo is not found the
fallback second parameter is added to the kvdb and then returned.

Get the kvo using it integer index

.. code:: python

    key_value_db.get_key_value_object(0)
    #<KeyValueObject@6034722440246165772:Key=Greet,Value=Hello World>

Get the kvo using it key

.. code:: python

    key_value_db.get_key_value_object("Greet")
    #<KeyValueObject@6034722440246165772:Key=Greet,Value=Hello World>

Get the kvo using it key with fallback kvo

.. code:: python

    key_value_object = KeyValueObject("Name", "Adewale Azeez")
    key_value_db.get_key_value_object("Name", key_value_object)
    #<KeyValueObject@6034722440246165772:Key=Name,Value=Adewale Azeez>

Get Like KeyValue Object
^^^^^^^^^^^^^^^^^^^^^^^^

Get a kvo by checking the kvdb for the kvo object that contains a part
of the key. If a fallback kvo is sent as second parameter then when the
request kvo is not found the fallback second parameter is added to the
kvdb and then returned.

Get a similar kvo using it key part

.. code:: python

    key_value_db.get_like_key_value_object("eet")
    #<KeyValueObject@6034722440246165772:Key=Greet,Value=Hello World>

Get a similar kvo using it key part with fallback kvo

.. code:: python

    key_value_object = KeyValueObject("Name", "Adewale Azeez")
    key_value_db.get_like_key_value_object("Nam", key_value_object)
    #<KeyValueObject@6034722440246165772:Key=Name,Value=Adewale Azeez>

Get
^^^

You can get a kvdb value using either the key or index. If the
corresponding value is not found, an empty string is added to the db and
then returned but not in the case when requested with the integer index.

If a fallback kvo is sent as second parameter then when the request key
is not found the fallback second parameter is added to the kvdb and then
value is returned. If a string value is sent as the second value it is
returned if the key is not found in the kvdb.

Get a value using it integer index

.. code:: python

    key_value_db.get(0)
    #"Hello World"

Get the value using it key

.. code:: python

    key_value_db.get("Greet")
    #"Hello World"

Get the kvo using it key with fallback value

.. code:: python

    key_value_db.get("Licence", "The MIT Licence")
    #"The MIT Licence"

Get the kvo using it key with fallback kvo

.. code:: python

    key_value_object = KeyValueObject("Licence", "The MIT Licence")
    key_value_db.get("Name", key_value_object)
    #"The MIT Licence"

Get Like
^^^^^^^^

Get a value by checking the kvdb for the kvo object that contains a part
of the key.

If a fallback kvo is sent as second parameter then when the request key
is not found the fallback second parameter is added to the kvdb and then
value is returned.

Get a value using it key part

.. code:: python

    key_value_db.get_like("eet")
    #"Hello World"

Get a value using it key part with fallback kvo

.. code:: python

    key_value_object = KeyValueObject("Licence", "The MIT Licence")
    key_value_db.get_like("Li", key_value_object)
    #"The MIT Licence"

Updating Data
~~~~~~~~~~~~~

There are various way to update a kvp in the kvdb, the value can be
changed directly or set to a new KeyValueObject. If you try to set a kvo
that does not exist in the kvdb using it key, it is added to the kvdb.

Set
^^^

The ``set`` method is used to change the value of the kvo using the
index of the kvo or a kvo key.

Set a kvo value using it index

.. code:: python

    key_value_db.set(0, "Hello World from thecarisma")
    #<KeyValueObject@603472244355765772:Key=Greet,Value=Hello World from thecarisma>

Set a kvo value using it key

.. code:: python

    key_value_db.set("Greet", "Hello World from thecarisma")
    #<KeyValueObject@603472244355765772:Key=Greet,Value=Hello World from thecarisma>

Set KeyValue Object
^^^^^^^^^^^^^^^^^^^

Completly change a KeyValueObject in the kvdb using either it index or
it key. The kvo is completly replaced which means unique fields like the
hashcode of the kvo changes. When the kvo is set using it key if the
corresponding kvo does not exist it is added into the kvdb. Note that
this method completly changes the kvo so it can be used to replace a
kvo.

Set a kvo using it index

.. code:: python

    key_value_object = KeyValueObject("Licence", "The MIT Licence")
    key_value_db.set_keyValueObject(0, key_value_object)
    #<KeyValueObject@6034545687687898767:Key=Licence,Value=The MIT Licence>

Set a kvo value using it key

.. code:: python

    key_value_object = KeyValueObject("Licence", "The MIT Licence")
    key_value_db.set_key_value_object("Greet", key_value_object)
    #<KeyValueObject@6034545687687898767:Key=Licence,Value=The MIT Licence>

Inserting Data
~~~~~~~~~~~~~~

A new kvp can be inserted by invoking the ``add`` method. The kvp can be
added using it key and value or by directly adding the KeyValueObject to
the kvdb.

Add a new kvp using the key and value

.. code:: python

    key_value_db.add("Key", "This is the value")

Add a new kvp using a new KeyValueObject

.. code:: python

    key_value_object = KeyValueObject("Key", "This is the value")
    key_value_db.add(key_value_object)

Removing Data
~~~~~~~~~~~~~

Remove a kvp completely from the kvdb using either it key of the integer
index. The kvp that was removed is returned from the method. If the
index does not exist out of bound error occur and if a kvo with the key
is not present nothing is done but an empty kvo is returned.

Remove a kvp using integer index

.. code:: python

    key_value_db.remove(0)
    #removes the first kvp in the kvdb
    #<KeyValueObject@6034722440246165772:Key=Greet,Value=Hello World>

Remove a kvp using it key

.. code:: python

    key_value_db.remove("Greet")
    #removes the first kvp in the kvdb
    #<KeyValueObject@6034722440246165772:Key=Greet,Value=Hello World>

Size, Clear, isEmpty
--------------------

Size
~~~~

Get the size of the kvo in the kvdb.

.. code:: python

    key_value_db.size()
    #4

Clear
~~~~~

Remove all the elements and kvo from the kvdb

.. code:: python

    key_value_db.clear()
    #key_value_db.size() = 0

isEmpty
~~~~~~~

Check whether the kvdb contains any kvo in it.

.. code:: python

    key_value_db.is_empty();
    #false

Saving collection
-----------------

The kvp collection kvdb can be inspected as a string using the
``__str__`` method. The returned value can be saved locally by writing
to a persistent storage or to a plain text file. The output of the
``__str__`` method is determined by the kvos, the seperator and the
delimeter.

.. code:: python

    key_value_db.__str__();
    #"Greet=Hello World,Project=KeyValueDB,Project=KeyValueDB,Licence=The MIT Licence"

Iterating collection
--------------------

The KeyValueDB object can be iterated natively using the ``for..in``
loop expression.

.. code:: python

    for kvo in key_value_db:
        #operate on the KeyValueObject

How it works
------------

KeyValueObject class contains the key and value field and the fields
setter and getter. The KeyValueObject is the main internal type used in
the KeyValueDB class.

In KeyValueDB the key value pair is stored in ``[KeyValueObject...]``
type, all search, updating and removal is done on the
``keyValueObjects`` in the class. The string sent as first parameter if
parsed into valid key value using the separator and delimiter fields.
The ``__str__`` method also parse the ``keyValueObjects`` content into a
valid string with regards to the separator and delimeter.

Contributing
------------

Before you begin contribution please read the contribution guide at
`CONTRIBUTING GUIDE <https://keyvaluedb.github.io/contributing.html>`__

You can open issue or file a request that only address problems in this
implementation on this repo, if the issue address the concepts of the
package then create an issue or rfc
`here <https://github.com/keyvaluedb/keyvaluedb.github.io/>`__

Support
-------

You can support some of this community as they make big impact in the
developement of people to get started with software engineering.

-  https://www.patreon.com/devcareer

License
-------

MIT License Copyright (c) 2019 Adewale Azeez - keyvaluedb
