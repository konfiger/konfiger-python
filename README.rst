
Light weight package to manage key value based configuration and data
files.

The notable use cases of this package is loading configuration file,
language file, preference setting in an application.

--------------

Table of content
----------------

-  `Installation <#installation>`__
-  `Examples <#examples>`__

   -  `Basic <#basic>`__
   -  `Write to disk <#write-to-disk>`__
   -  `Get Types <#get-types>`__
   -  `Lazy Loading <#lazy-loading>`__
   -  `Seperator and delimeter <#seperator-and-delimeter>`__
   -  `Read file with Stream <#read-file-with-stream>`__
   -  `Read String with Stream <#read-string-with-stream>`__
   -  `Skip Comment entries <#Skip-comment-entries>`__
   -  `Resolve Object <#resolve-object>`__
   -  `Dissolve Object <#dissolve-object>`__
   -  `Multiline value <#multiline-value>`__

-  `Native Object Attachement <#native-object-attachement>`__

   -  `match_get_key <#matchgetkey>`__
   -  `match_put_key <#matchputkey>`__

-  `API Documentations <#api-documentations>`__

   -  `KonfigerStream <#konfigerstream>`__
   -  `Konfiger <#konfiger>`__

      -  `Fields <#fields>`__
      -  `Functions <#functions>`__

-  `Usage <#usage>`__

   -  `Initialization <#initialization>`__
   -  `Inserting <#inserting>`__
   -  `Finding <#finding>`__
   -  `Updating <#updating>`__
   -  `Removing <#removing>`__
   -  `Saving to disk <#saving-to-disk>`__

-  `How it works <#how-it-works>`__
-  `Contributing <#contributing>`__
-  `Support <#support>`__
-  `License <#license>`__

Installation
------------

Module name on PyPi is konfiger.

Using pip:

.. code:: bash

   pip install konfiger

Installing from source:

.. code:: bash

   git clone https://github.com/konfiger/konfiger-python.git
   cd konfiger-python
   pip install .

Examples
--------

Basic
~~~~~

The following example load from file, add an entry, remove an entry and
iterate all the key value entries

.. code:: python

   from konfiger import from_file

   #initialize the key-value from file
   kon = from_file('test/test.config.ini', True)

   #add a string
   kon.put_string("Greet", "Hello World")

   #get an object
   print(kon.get("Greet"))

   #remove an object
   kon.remove("Greet")

   #add an String
   kon.put_string("What", "i don't know what to write here");

   for key, value in kon.entries():
       print('[' + key + ', ' + value + ']')

Write to disk
~~~~~~~~~~~~~

Initialize an empty konfiger object and populate it with random data,
then save it to a file

.. code:: python

   from konfiger import from_string
   import random

   random_values = [ 'One', 'Two', 'Three', 'Four', 'Five' ]
   kon = from_string("", False)

   for i in range(200):
       rand = random.randint(0, len(random_values) - 1)
       kon.put_string(str(i), random_values[rand])
       
   kon.save('test/konfiger.conf')

Get Types
~~~~~~~~~

Load the entries as string and get them as a True type.

.. code:: python

   from konfiger import from_string

   kon = from_string("""
   String=This is a string
   Number=215415245
   Float=56556.436746
   Boolean=True
   """, False)

   str_ = kon.get_string("String")
   num_ = kon.get_long("Number")
   flo_ = kon.get_float("Float")
   bool_ = kon.get_boolean("Boolean")

   print(type(str_))
   print(type(num_))
   print(type(flo_))
   print(type(bool_))

Lazy Loading
~~~~~~~~~~~~

The lazyLoad parameter is useful for progressively read entries from a
large file. The next example shows initializing from a file with so much
key value entry with lazy loading:

The content of ``test/konfiger.conf`` is

::

   Ones=11111111111
   Twos=2222222222222
   Threes=3333333333333
   Fours=444444444444
   Fives=5555555555555

.. code:: python

   from konfiger import from_file

   kon = from_file('test/konfiger.conf', #the file pth
                           True #lazyLoad True
                           )
   #at this point nothing is read from the file

   #the size of konfiger is 0 even if the file contains over 1000 entries

   #the key 'Twos' is at the second line in the file, therefore two entry has 
   #been read to get the value.
   print(kon.get("Twos"))

   #the size becomes 2,

   #to read all the entries simply call the toString() method
   print(str(kon))

   #now the size is equal to the entry
   print(len(kon))

Seperator and delimeter
~~~~~~~~~~~~~~~~~~~~~~~

Initailize a konfiger object with default seperator and delimeter then
change the seperator and selimeter at runtime

.. code:: python

   from konfiger import from_file

   kon = from_file('test/konfiger.conf', False)
   kon.set_delimeter('?')
   kon.set_seperator(',')

   print(str(kon))

Read file with Stream
~~~~~~~~~~~~~~~~~~~~~

Read a key value file using the progressive
`KonfigerStream <https://github.com/konfiger/konfiger-python/blob/master/src/konfiger_stream.py>`__,
each scan returns the current key value array ``('key', 'value')``

.. code:: python

   from konfiger import file_stream

   k_stream = file_stream('test/konfiger.conf')
   while (k_stream.has_next()):
       entry = k_stream.next()
       print(entry)

Read String with Stream
~~~~~~~~~~~~~~~~~~~~~~~

Read a key value string using the progressive
`KonfigerStream <https://github.com/konfiger/konfiger-python/blob/master/src/konfiger_stream.py>`__,
each scan returns the current key value array ``('key', 'value')``

.. code:: python

   from konfiger import string_stream

   k_stream = string_stream("""
   String=This is a string
   Number=215415245
   Float=56556.436746
   Boolean=True
   """)

   while (k_stream.has_next()):
       entry = k_stream.next()
       print(entry)

Skip Comment entries
~~~~~~~~~~~~~~~~~~~~

Read all the key value entry using the stream and skipping all commented
entries. The default comment prefix is ``//`` but in the example below
the commented entries starts with ``#`` so the prefix is changed. The
same thing happen if the key value entry is loaded from file.

.. code:: python

   from konfiger import string_stream

   k_stream = string_stream("""
   String=This is a string
   #Number=215415245
   Float=56556.436746
   #Boolean=True
   """)
   k_stream.set_comment_prefix("#")

   while (k_stream.has_next()):
       entry = k_stream.next()
       print(entry)

Resolve Object
~~~~~~~~~~~~~~

The example below attach a python object to a konfiger object, whenever
the value of the konfiger object changes the attached object entries is
also updated.

For the file properties.conf

::

   project = konfiger
   author = Adewale Azeez
   islibrary = True

.. code:: python

   from konfiger import from_file

   class Properties:
       project = ""
       author = ""
       islibrary = False

   kon = from_file('properties.conf')
   properties = Properties()
   kon.resolve(properties)

   print(properties.project) # konfiger
   print(properties.author) # Adewale Azeez
   print(properties.islibrary) # True
   kon.put("project", "konfiger-python")
   print(properties.project) # konfiger-python

Dissolve Object
~~~~~~~~~~~~~~~

The following snippet reads the value of a python object into the
konfiger object, the object is not attached to konfiger unlike resolve
function.

.. code:: python

   from konfiger import from_string

   class Properties:
       project = "konfiger"
       author = "Adewale"
       islibrary = True

   kon = from_string('')
   kon.dissolve(Properties())

   print(kon.get("project")) # konfiger
   print(kon.get("author")) # Adewale Azeez
   print(kon.get_boolean("islibrary")) # True

Multiline value
~~~~~~~~~~~~~~~

Konfiger stream allow multiline value. If the line ends with ``\`` the
next line will be parse as the continuation and the leading spaces will
be trimmed. The continuation character chan be changed like the example
below the continuation character is changed from ``\`` to ``+``.

for the file test.contd.conf

::

   Description = This project is the closest thing to Android +
                 Shared Preference in other languages +
                 and off the Android platform.
   ProjectName = konfiger

.. code:: python

   from konfiger import file_stream

   ks = file_stream("test.contd.conf")
   ks.set_continuation_char('+')
   print(ks.next()[1])
   print(ks.next()[1])

Native Object Attachement
-------------------------

This feature of the project allow seamless integration with the konfiger
entries by eliminating the need for writing ``get*("")`` everytime to
read a value into a variable or writing lot of ``put*()`` to add an
entry.

The two function ``resolve`` is used to attach an object. resolve
function integrate the object such that the entries in konfiger will be
assigned to the matching key in the object. See the
`resolve <#resolve-object>`__ and `dissolve <#dissolve-object>`__
examples above.

In a case where the object keys are different from the entries keys in
the konfiger object the function ``match_get_key`` can be declared in
the object to match the key when setting the object entries values, and
the function ``match_put_key`` is called when setting the konfiger
entries from the object.

Konfiger is aware of the type of an object field, if the type of a field
is boolean the entry value will be parsed as boolean and assigned to the
field.

For the file English.lang

::

   LoginTitle = Login Page
   AgeInstruction = You must me 18 years or above to register
   NewsletterOptin = Signup for our weekly news letter
   ShouldUpdate = True

For an object which as the same key as the konfiger entries above there
is no need to declare the match_get_key or match_put_key in the object.
Resolve example

.. code:: python

   from konfiger import from_file

   class PageProps:
       LoginTitle = ""
       AgeInstruction = ""
       NewsletterOptin = ""
       ShouldUpdate = False

       def __str__(self):
           return "LoginTitle=" + self.LoginTitle + ",AgeInstruction=" + self.AgeInstruction + ",NewsletterOptin=" + self.NewsletterOptin + ",ShouldUpdate=" + str(self.ShouldUpdate)

   kon = from_file('English.lang')
   page_props = PageProps()
   kon.resolve(page_props)
   print(page_props)

Dissolve example

.. code:: python

   from konfiger import from_string

   class PageProps:
       LoginTitle = "Login Page"
       AgeInstruction = "You must me 18 years or above to register"
       NewsletterOptin = "Signup for our weekly news letter"
       ShouldUpdate = True

   kon = from_string('')
   kon.dissolve(PageProps())
   print(str(kon))

match_get_key
~~~~~~~~~~~~~

If the identifier in the object keys does not match the above entries
key the object will not be resolved. For example loginTitle does not
match LoginTitle, the match_get_key can be used to map the variable key
to the konfiger entry key. The following example map the object key to
konfiger entries key.

.. code:: python

   from konfiger import from_file

   class PageProps:
       loginTitle = ""
       ageInstruct = ""
       NewsletterOptin = ""
       
       def match_get_key(self, key):
           if key == "loginTitle":
               return "LoginTitle"
           elif key == "ageInstruct":
               return "AgeInstruction"
               
       def __str__(self):
           return "loginTitle=" + self.loginTitle + ",ageInstruct=" + self.ageInstruct + ",NewsletterOptin=" + self.NewsletterOptin

   kon = from_file('English.lang')
   page_props = PageProps()
   kon.resolve(page_props)
   print(page_props)

The way the above code snippet works is that when iterating the object
keys if check if the function match_get_key is present in the object if
it is present the key is sent as parameter to the match_get_key and the
returned value is used to get the value from konfiger, if the
match_get_key does not return anything the object key is used to get the
value from konfiger (as in the case of NewsletterOptin).

   During the resolve or dissolve process if the entry value is function
   it is skipped even if it key matches

For dissolving an object the method match_get_key is invoked to find the
actual key to use to add the entry in konfiger, if the object does not
declare the match_get_key function the entries will be added to konfiger
as it is declared. The following example similar to the one above but
dissolves an object into konfiger.

.. code:: python

   from konfiger import from_string

   class PageProps:
       loginTitle = "Login Page"
       ageInstruct = "You must me 18 years or above to register"
       NewsletterOptin = "Signup for our weekly news letter"
       
       def match_get_key(self, key):
           if key == "loginTitle":
               return "LoginTitle"
           elif key == "ageInstruct":
               return "AgeInstruction"
               
       def __str__(self):
           return "loginTitle=" + self.loginTitle + ",ageInstruct=" + self.ageInstruct + ",NewsletterOptin=" + self.NewsletterOptin

   kon = from_string('')
   kon.dissolve(PageProps())
   print(str(kon))

match_put_key
~~~~~~~~~~~~~

The match_put_key is invoked when an entry value is changed or when a
new entry is added to konfiger. The match_put_key is invoked with the
new entry key and checked in the object match_put_key (if decalred), the
returned value is what is set in the object. E.g. if an entry
``[Name, Thecarisma]`` is added to konfiger the object match_put_key is
invoked with the parameter ``Name`` the returned value is used to set
the corresponding object entry.

.. code:: python

   from konfiger import from_string

   class PageProps:
       loginTitle = ""
       ageInstruct = ""
       NewsletterOptin = ""
       
       def match_put_key(self, key):
           if key == "LoginTitle":
               return "loginTitle"
           elif key == "AgeInstruction":
               return "ageInstruct"

   kon = from_string('')
   page_props = PageProps()
   kon.resolve(page_props)

   kon.put("LoginTitle", "Login Page")
   kon.put("AgeInstruction", "You must me 18 years or above to register")
   kon.put("NewsletterOptin", "Signup for our weekly news letter")
   print(page_props.loginTitle)
   print(page_props.ageInstruct)
   print(page_props.NewsletterOptin)

Konfiger does not create new entry in an object it just set existing
values. Konfiger only change the value in an object if the key is
defined

   Warning!!! The values resolved is not typed so if the entry initial
   value is an integer the resolved value will be a string. All resolved
   value is string, you will need to do the type conversion by your
   self.

If your entry keys is the same as the object keys you don"t need to
declare the match_get_key or match_put_key function in the object.

Usage
-----

Initialization
~~~~~~~~~~~~~~

The main Konfiger contructor is not exported from the package, the two
functions are exported for initialization, ``from_string`` and
``from_file``. The from_string function creates a Konfiger object from a
string with valid key value entry or from empty string, the from_file
function creates the Konfiger object from a file, the two functions
accept a cumpulsory second parameter ``lazyLoad`` which indicates
whether to read all the entry from the file or string suring
initialization. The lazyLoad parameter is useful for progressively read
entries from a large file. The two initializing functions also take 2
extra optional parameters ``delimeter`` and ``seperator``. If the third
and fourth parameter is not specified the default is used, delimeter =
``=``, seperator = ``\n``. If the file or string has different delimeter
and seperator always send the third and fourth parameter.

The following initializer progressively read the file when needed

.. code:: python

   konfiger = from_file('test/konfiger.conf', True)

The following initializer read all the entries from file at once

.. code:: python

   konfiger = from_file('test/konfiger.conf', False)

The following initializer read all the entries from string when needed

.. code:: python

   konfiger = from_string("""
   Ones=11111111111
   Twos=2222222222222
   """, True)

The following initializer read all the entries from String at once

.. code:: python

   konfiger = from_string("""
   Ones=11111111111
   Twos=2222222222222
   """, False)

Initialize a string which have custom delimeter and seperator

.. code:: python

   konfiger = from_string("""Ones:11111111111,Twos:2222222222222""", 
                                   False, 
                                   ':',
                                   ',')

Inserting
~~~~~~~~~

The following types can be added into the object, int, float, long,
boolean, object and string.

To add any object into the entry use the ``put`` method as it check the
value type and properly get it string value

.. code:: python

   konfiger.put("String", "This is a string")
   konfiger.put("Long", 143431423)
   konfiger.put("Boolean", True)
   konfiger.put("Float", 12.345)

The ``put`` method do a type check on the value and calls the
appropriate put method e.g ``konfiger.put("Boolean", True)`` will result
in a call to ``konfiger.put_boolean("Boolean", True)``. The following
method are avaliable to directly add the value according to the type,
``put_string``, ``put_boolean``, ``put_long`` and ``putInt``. The
previous example can be re-written as:

.. code:: python

   konfiger.put_string("String", "This is a string")
   konfiger.put_long("Long", 143431423)
   konfiger.put_boolean("Boolean", True)
   konfiger.put_float("Float", 12.345)

Finding
~~~~~~~

There are various ways to get the value from the konfiger object, the
main ``get`` method and ``get_string`` method both returns a string
type, the other get methods returns specific types

.. code:: python

   konfiger.get("String")

To get specific type from the object use the following methods,
``get_string``, ``get_boolean``, ``get_long``, ``get_float`` and
``getInt``.

.. code:: python

   konfiger.get_string("String")
   konfiger.get_long("Long")
   konfiger.get_boolean("Boolean")
   konfiger.get_float("Float")

If the requested entrr does not exist a null/undefined value is
returned, to prevent that a fallback value should be sent as second
parameter incase the key is not found the second parameter will be
returned.

.. code:: python

   konfiger.get("String", "Default Value")
   konfiger.get_boolean("Boolean", False)

If the konfiger is initialized with lazy loading enabled if the get
method is called the stream will start reading until the key is found
and the stream is paused again, if the key is not found the stream will
read to end.

Updating
~~~~~~~~

The ``put`` method can be used to add new entry or to update an already
existing entry in the object. The ``update_at`` method is usefull for
updating a value using it index instead of key

.. code:: python

   konfiger.update_at(0, "This is an updated string")

Removing
~~~~~~~~

The ``remove`` method removes a key value entry from the konfiger, it
returns True if an entry is removed and False if no entry is removed.
The ``remove`` method accept either key(string) or index(int) of the
entry.

.. code:: python

   konfiger.remove("String")
   konfiger.remove(0)

Saving to disk
~~~~~~~~~~~~~~

Every operation on the konfiger object is done in memory to save the
updated entries in a file call the ``save`` method with the file path to
save the entry. If the konfiger is initiated from file then there is no
need to add the file path to the ``save`` method, the entries will be
saved to the file path used during initialization.

.. code:: python

   konfiger.save("test/test.config.ini")

in case of load from file, the save will write the entries to
*test/test.config.ini*.

.. code:: python

   #...
   var konfiger = from_file('test/test.config.ini', True)
   #...
   konfiger.save()

API Documentations
------------------

Even though python is weakly type the package does type checking to
ensure wrong datatype is not passed into the functions.

KonfigerStream
~~~~~~~~~~~~~~

+-------------------------------------+--------------------------------+
| Function                            | Description                    |
+=====================================+================================+
| def file_stream(file_path,          | Initialize a new               |
| delimeter = "=", seperator =        | KonfigerStream object from the |
| "\n", err_tolerance =               | filePath. It throws en         |
| False)                              | exception if the filePath does |
|                                     | not exist or if the delimeter  |
|                                     | or seperator is not a single   |
|                                     | character. The last parameter  |
|                                     | is boolean if True the stream  |
|                                     | is error tolerant and does not |
|                                     | throw any exception on invalid |
|                                     | entry, only the first          |
|                                     | parameter is cumpulsory.       |
+-------------------------------------+--------------------------------+
| def string_stream(raw_string,       | Initialize a new               |
| delimeter = "=", seperator =        | KonfigerStream object from a   |
| "\n", err_tolerance =               | string. It throws en exception |
| False)                              | if the rawString is not a      |
|                                     | string or if the delimeter or  |
|                                     | seperator is not a single      |
|                                     | character. The last parameter  |
|                                     | is boolean if True the stream  |
|                                     | is error tolerant and does not |
|                                     | throw any exception on invalid |
|                                     | entry, only the first          |
|                                     | parameter is cumpulsory.       |
+-------------------------------------+--------------------------------+
| def has_next(self)                  | Check if the KonfigerStream    |
|                                     | still has a key value entry,   |
|                                     | returns True if there is still |
|                                     | entry, returns False if there  |
|                                     | is no more entry in the        |
|                                     | KonfigerStream                 |
+-------------------------------------+--------------------------------+
| def next(self)                      | Get the next Key Value array   |
|                                     | from the KonfigerStream is it  |
|                                     | still has an entry. Throws an  |
|                                     | error if there is no more      |
|                                     | entry. Always use              |
|                                     | ``has_next()`` to check if     |
|                                     | there is still an entry in the |
|                                     | stream.                        |
+-------------------------------------+--------------------------------+
| def is_trimming_key(self)           | Check if the stream is         |
|                                     | configured to trim key, True   |
|                                     | by default                     |
+-------------------------------------+--------------------------------+
| def set_trimming_key(self,          | Change the stream to           |
| trimming_key)                       | enable/disable key trimming    |
+-------------------------------------+--------------------------------+
| def is_trimming_value(self)         | Check if the stream is         |
|                                     | configured to trim entry       |
|                                     | value, True by default         |
+-------------------------------------+--------------------------------+
| def set_trimming_value(self,        | Change the stream to           |
| trimming_value)                     | enable/disable entry value     |
|                                     | trimming                       |
+-------------------------------------+--------------------------------+
| def get_comment_prefix(self)        | Get the prefix string that     |
|                                     | indicate a pair entry if       |
|                                     | commented                      |
+-------------------------------------+--------------------------------+
| def set_comment_prefix(self,        | Change the stream comment      |
| comment_prefix)                     | prefix, any entry starting     |
|                                     | with the comment prefix will   |
|                                     | be skipped. Comment in         |
|                                     | KonfigerStream is relative to  |
|                                     | the key value entry and not    |
|                                     | relative to a line.            |
+-------------------------------------+--------------------------------+
| def set_continuation_char(self,     | Set the character that         |
| continuation_char)                  | indicates to the stream to     |
|                                     | continue reading for the entry |
|                                     | value on the next line. The    |
|                                     | follwoing line leading spaces  |
|                                     | is trimmed. The default is     |
|                                     | ``\``                          |
+-------------------------------------+--------------------------------+
| def get_continuation_char(self)     | Get the continuation character |
|                                     | used in the stream.            |
+-------------------------------------+--------------------------------+
| def                                 | Validate the existence of the  |
| validate_file_existence(file_path)  | specified file path if it does |
|                                     | not exist an exception is      |
|                                     | thrown                         |
+-------------------------------------+--------------------------------+
| def error_tolerance(self,           | Enable or disable the error    |
| err_tolerance)                      | tolerancy property of the      |
|                                     | konfiger, if enabled no        |
|                                     | exception will be throw even   |
|                                     | when it suppose to there for   |
|                                     | it a bad idea but useful in a  |
|                                     | fail safe environment.         |
+-------------------------------------+--------------------------------+
| def is_error_tolerant(self)         | Check if the konfiger object   |
|                                     | errTolerance is set to True.   |
+-------------------------------------+--------------------------------+

Konfiger
~~~~~~~~

Fields
^^^^^^

=================== ===================================================
Field               Description
=================== ===================================================
GLOBAL_MAX_CAPACITY The number of datas the konfiger can take, 10000000
=================== ===================================================

Functions
^^^^^^^^^

+-------------------------------------+--------------------------------+
| Function                            | Description                    |
+=====================================+================================+
| def from_file(file_path,            | Create the konfiger object     |
| lazy_load=True, delimeter="=",      | from a file, the first(string) |
| seperator="\n")                     | parameter is the file path,    |
|                                     | the second parameter(boolean)  |
|                                     | indicates whether to read all  |
|                                     | the entry in the file in the   |
|                                     | constructor or when needed,    |
|                                     | the third param(char) is the   |
|                                     | delimeter and the fourth       |
|                                     | param(char) is the seperator.  |
|                                     | This creates the konfiger      |
|                                     | object from call to            |
|                                     | ``fromStre                     |
|                                     | am(konfigerStream, lazyLoad)`` |
|                                     | with the konfigerStream        |
|                                     | initialized with the filePath  |
|                                     | parameter. The new Konfiger    |
|                                     | object is returned.            |
+-------------------------------------+--------------------------------+
| def from_string(raw_string,         | Create the konfiger object     |
| lazy_load=True, delimeter="=",      | from a string, the first       |
| seperator="\n")                     | parameter is the String(can be |
|                                     | empty), the second boolean     |
|                                     | parameter indicates whether to |
|                                     | read all the entry in the file |
|                                     | in the constructor or when     |
|                                     | needed, the third param is the |
|                                     | delimeter and the fourth param |
|                                     | is the seperator. The new      |
|                                     | Konfiger object is returned.   |
+-------------------------------------+--------------------------------+
| def from_stream(konfiger_stream,    | Create the konfiger object     |
| lazy_load=True)                     | from a KonfigerStream object,  |
|                                     | the second boolean parameter   |
|                                     | indicates whether to read all  |
|                                     | the entry in the file in the   |
|                                     | constructor or when needed     |
|                                     | this make data loading         |
|                                     | progressive as data is only    |
|                                     | loaded from the file when put  |
|                                     | or get until the Stream        |
|                                     | reaches EOF. The new Konfiger  |
|                                     | object is returned.            |
+-------------------------------------+--------------------------------+
| def put(self, key, value)           | Put any object into the        |
|                                     | konfiger. if the second        |
|                                     | parameter is a python Object,  |
|                                     | ``JSON.stringify`` will be     |
|                                     | used to get the string value   |
|                                     | of the object else the         |
|                                     | appropriate put\* method will  |
|                                     | be called. e.g                 |
|                                     | ``put('Name', 'Adewale')``     |
|                                     | will result in the call        |
|                                     | ``pu                           |
|                                     | t_string('Name', 'Adewale')``. |
+-------------------------------------+--------------------------------+
| def put_string(self, key, value)    | Put a String into the          |
|                                     | konfiger, the second parameter |
|                                     | must be a string.              |
+-------------------------------------+--------------------------------+
| def put_boolean(self, key, value)   | Put a Boolean into the         |
|                                     | konfiger, the second parameter |
|                                     | must be a Boolean.             |
+-------------------------------------+--------------------------------+
| def put_long(self, key, value)      | Put a Long into the konfiger,  |
|                                     | the second parameter must be a |
|                                     | Number.                        |
+-------------------------------------+--------------------------------+
| def put_int(self, key, value)       | Put a Int into the konfiger,   |
|                                     | alias for                      |
|                                     | ``put_long(self, key, value)``.|
+-------------------------------------+--------------------------------+
| def put_float(self, key, value)     | Put a Float into the konfiger, |
|                                     | the second parameter must be a |
|                                     | Float                          |
+-------------------------------------+--------------------------------+
| def put_double(self, key, value)    | Put a Double into the          |
|                                     | konfiger, the second parameter |
|                                     | must be a Double               |
+-------------------------------------+--------------------------------+
| def put_comment(self, the_comment)  | Put a literal comment into the |
|                                     | konfiger, it simply add the    |
|                                     | comment prefix as key and      |
|                                     | value to the entries           |
|                                     | e.g ``ko                       |
|                                     | n.put_comment("Hello World")`` |
|                                     | add the entry                  |
|                                     | ``//:Hello World``             |
+-------------------------------------+--------------------------------+
| def keys(self)                      | Get all the keys entries in    |
|                                     | the konfiger object in         |
|                                     | iterable array list            |
+-------------------------------------+--------------------------------+
| def values(self)                    | Get all the values entries in  |
|                                     | the konfiger object in         |
|                                     | iterable array list            |
+-------------------------------------+--------------------------------+
| def entries(self)                   | Get all the entries in the     |
|                                     | konfiger in a                  |
|                                     | ``[['Key', 'Value'], ...]``    |
+-------------------------------------+--------------------------------+
| def get(self, key,                  | Get a value as string, the     |
| default_value=None)                 | second parameter is optional   |
|                                     | if it is specified it is       |
|                                     | returned if the key does not   |
|                                     | exist, if the second parameter |
|                                     | is not specified ``undefined`` |
|                                     | will be returned               |
+-------------------------------------+--------------------------------+
| def get_string(self, key,           | Get a value as string, the     |
| default_value="")                   | second(string) parameter is    |
|                                     | optional if it is specified it |
|                                     | is returned if the key does    |
|                                     | not exist, if the second       |
|                                     | parameter is not specified     |
|                                     | empty string will be returned. |
+-------------------------------------+--------------------------------+
| def get_boolean(self, key,          | Get a value as boolean, the    |
| default_value=False)                | second(Boolean) parameter is   |
|                                     | optional if it is specified it |
|                                     | is returned if the key does    |
|                                     | not exist, if the second       |
|                                     | parameter is not specified     |
|                                     | ``False`` will be returned.    |
|                                     | When trying to cast the value  |
|                                     | to boolean if an error occur   |
|                                     | an exception will be thrown    |
|                                     | except if error tolerance is   |
|                                     | set to True then False will be |
|                                     | returned.                      |
+-------------------------------------+--------------------------------+
| def get_long(self, key,             | Get a value as Number, the     |
| default_value=0)                    | second(Number) parameter is    |
|                                     | optional if it is specified it |
|                                     | is returned if the key does    |
|                                     | not exist, if the second       |
|                                     | parameter is not specified     |
|                                     | ``0`` will be returned. When   |
|                                     | trying to cast the value to    |
|                                     | Number if an error occur an    |
|                                     | exception will be thrown       |
|                                     | except if error tolerance is   |
|                                     | set to True then ``0`` will be |
|                                     | returned.                      |
+-------------------------------------+--------------------------------+
| def get_int(self, key,              | Get a value as Number, alias   |
| default_value=0)                    | for                            |
|                                     | ``def                          |
|                                     | get_long(key, defaultValue)``. |
+-------------------------------------+--------------------------------+
| def get_float(self, key,            | Get a value as Float, the      |
| default_value=0.0)                  | second(Float) parameter is     |
|                                     | optional if it is specified it |
|                                     | is returned if the key does    |
|                                     | not exist, if the second       |
|                                     | parameter is not specified     |
|                                     | ``0.0`` will be returned. When |
|                                     | trying to cast the value to    |
|                                     | Float if an error occur an     |
|                                     | exception will be thrown       |
|                                     | except if error tolerance is   |
|                                     | set to True then ``0.0`` will  |
|                                     | be returned.                   |
+-------------------------------------+--------------------------------+
| def get_double(self, key,           | Get a value as Double, the     |
| default_value=0.0)                  | second(Double) parameter is    |
|                                     | optional if it is specified it |
|                                     | is returned if the key does    |
|                                     | not exist, if the second       |
|                                     | parameter is not specified     |
|                                     | ``0.0`` will be returned. When |
|                                     | trying to cast the value to    |
|                                     | Double if an error occur an    |
|                                     | exception will be thrown       |
|                                     | except if error tolerance is   |
|                                     | set to True then ``0.0`` will  |
|                                     | be returned.                   |
+-------------------------------------+--------------------------------+
| def remove(self, key_index)         | Remove a key value entry at a  |
|                                     | particular index. Returns the  |
|                                     | value of the entry that was    |
|                                     | removed.                       |
+-------------------------------------+--------------------------------+
| def remove(self, key_index)         | Remove a key value entry using |
|                                     | the entry Key. Returns the     |
|                                     | value of the entry that was    |
|                                     | removed.                       |
+-------------------------------------+--------------------------------+
| def append_string(self, raw_string, | Append new data to the         |
| delimeter=None, seperator=None)     | konfiger from a string. If the |
|                                     | Konfiger is initialized with   |
|                                     | lazy loading all the data will |
|                                     | be loaded before the entries   |
|                                     | from the new string is added.  |
+-------------------------------------+--------------------------------+
| def append_file(self, file_path,    | Read new datas from the file   |
| delimeter=None, seperator=None)     | path and append. If the        |
|                                     | Konfiger is initialized with   |
|                                     | lazy loading all the data will |
|                                     | be loaded before the entries   |
|                                     | from the new string is added.  |
+-------------------------------------+--------------------------------+
| def save(self, file_path=None)      | Save the konfiger datas into a |
|                                     | file. The argument filePath is |
|                                     | optional if specified the      |
|                                     | entries is writtent to the     |
|                                     | filePath else the filePath     |
|                                     | used to initialize the         |
|                                     | Konfiger object is used and if |
|                                     | the Konfiger is initialized    |
|                                     | ``from_string`` and the        |
|                                     | filePath is not specified an   |
|                                     | exception is thrown. This does |
|                                     | not clear the already added    |
|                                     | entries.                       |
+-------------------------------------+--------------------------------+
| def get_seperator(self)             | Get seperator char that        |
|                                     | seperate the key value entry,  |
|                                     | default is ``\n``.             |
+-------------------------------------+--------------------------------+
| def get_delimeter(self)             | Get delimeter char that        |
|                                     | seperated the key from it      |
|                                     | value, default is ``=``.       |
+-------------------------------------+--------------------------------+
| def set_seperator(self, seperator)  | Change seperator char that     |
|                                     | seperate the datas, note that  |
|                                     | the file is not updates, to    |
|                                     | change the file call the       |
|                                     | ``save()`` function. If the    |
|                                     | new seperator is different     |
|                                     | from the old one all the       |
|                                     | entries values will be re      |
|                                     | parsed to get the new proper   |
|                                     | values, this process can take  |
|                                     | time if the entries is much.   |
+-------------------------------------+--------------------------------+
| def set_delimeter(self, delimeter)  | Change delimeter char that     |
|                                     | seperated the key from object, |
|                                     | note that the file is not      |
|                                     | updates, to change the file    |
|                                     | call the ``save()`` function   |
+-------------------------------------+--------------------------------+
| def set_case_sensitivity(self,      | change the case sensitivity of |
| case_sensitive)                     | the konfiger object, if True   |
|                                     | ``get("Key")`` and             |
|                                     | ``get("key")`` will return     |
|                                     | different value, if False same |
|                                     | value will be returned.        |
+-------------------------------------+--------------------------------+
| def is_case_sensitive(self)         | Return True if the konfiger    |
|                                     | object is case sensitive and   |
|                                     | False if it not case sensitive |
+-------------------------------------+--------------------------------+
| def ``__len__``\ (self)             | Get the total size of key      |
|                                     | value entries in the konfiger  |
+-------------------------------------+--------------------------------+
| def clear(self)                     | clear all the key value        |
|                                     | entries in the konfiger. This  |
|                                     | does not update the file call  |
|                                     | the ``save`` method to update  |
|                                     | the file                       |
+-------------------------------------+--------------------------------+
| def is_empty(self)                  | Check if the konfiger does not |
|                                     | have an key value entry.       |
+-------------------------------------+--------------------------------+
| void update_at(index, value)        | Update the value at the        |
|                                     | specified index with the new   |
|                                     | string value, throws an error  |
|                                     | if the index is OutOfRange     |
+-------------------------------------+--------------------------------+
| def contains(self, key)             | Check if the konfiger contains |
|                                     | a key                          |
+-------------------------------------+--------------------------------+
| def enable_cache(self,              | Enable or disable caching,     |
| enable_cache _)                     | caching speeds up data search  |
|                                     | but can take up space in       |
|                                     | memory (very small though).    |
|                                     | Using ``get_string`` method to |
|                                     | fetch vallue **99999999999**   |
|                                     | times with cache disabled      |
|                                     | takes over 1hr and with cache  |
|                                     | enabled takes 20min.           |
+-------------------------------------+--------------------------------+
| def ``__str__``\ (self)             | All the kofiger datas are      |
|                                     | parsed into valid string with  |
|                                     | regards to the delimeter and   |
|                                     | seprator, the result of this   |
|                                     | method is what get written to  |
|                                     | file in the ``save`` method.   |
|                                     | The result is cached and       |
|                                     | calling the method while the   |
|                                     | no entry is added, deleted or  |
|                                     | updated just return the last   |
|                                     | result instead of parsing the  |
|                                     | entries again.                 |
+-------------------------------------+--------------------------------+
| def resolve(self, obj)              | Attach an object to konfiger,  |
|                                     | on attachment the values of    |
|                                     | the entries in the object will |
|                                     | be set to the coresponding     |
|                                     | value in konfiger. The object  |
|                                     | can have the ``match_get_key`` |
|                                     | function which is called with  |
|                                     | a key in konfiger to get the   |
|                                     | value to map to the entry and  |
|                                     | the function ``match_put_key`` |
|                                     | to check which value to fetch  |
|                                     | from the object to put into    |
|                                     | konfiger.                      |
+-------------------------------------+--------------------------------+
| def dissolve(self, obj)             | Each string fields in the      |
|                                     | object will be put into        |
|                                     | konfiger. The object can have  |
|                                     | the ``match_get_key`` function |
|                                     | which is called with a key in  |
|                                     | konfiger to get the value to   |
|                                     | map to the entry. This does    |
|                                     | not attach the object.         |
+-------------------------------------+--------------------------------+
| def attach(self, obj)               | Attach an object to konfiger   |
|                                     | without dissolving it field    |
|                                     | into konfiger or setting it    |
|                                     | fields to a matching konfiger  |
|                                     | entry. Use this if the values  |
|                                     | in an object is to be left     |
|                                     | intact but updated if a        |
|                                     | matching entry in konfiger     |
|                                     | changes.                       |
+-------------------------------------+--------------------------------+
| def detach(self)                    | Detach the object attached to  |
|                                     | konfiger when the resolve      |
|                                     | function is called. The        |
|                                     | detached object is returned.   |
+-------------------------------------+--------------------------------+

How it works
------------

Konfiger stream progressively load the key value entry from a file or
string when needed, it uses two method ``has_next`` which check if there
is still an entry in the stream and ``next`` for the current key value
entry in the stream.

In Konfiger the key value pair is stored in a ``map``, all search
updating and removal is done on the ``konfiger_objects`` in the class.
The string sent as first parameter if parsed into valid key value using
the separator and delimiter fields and if loaded from file it content is
parsed into valid key value pair. The ``toString`` method also parse the
``konfiger_objects`` content into a valid string with regards to the
separator and delimeter. The value is properly escaped and unescaped.

The ``save`` function write the current ``Konfiger`` to the file, if the
file does not exist it is created if it can. Everything is written in
memory and is disposed on app exit hence it important to call the
``save`` function when nessasary.

Contributing
------------

Before you begin contribution please read the contribution guide at
`CONTRIBUTING
GUIDE <https://github.com/konfiger/konfiger.github.io/blob/master/CONTRIBUTING.MD>`__

You can open issue or file a request that only address problems in this
implementation on this repo, if the issue address the concepts of the
package then create an issue or rfc
`here <https://github.com/konfiger/konfiger.github.io/>`__

Support
-------

You can support some of this community as they make big impact in the
training of individual to get started with software engineering and open
source contribution.

-  https://www.patreon.com/devcareer

License
-------

MIT License Copyright (c) 2020 `Adewale
Azeez <https://twitter.com/iamthecarisma>`__ - konfiger
