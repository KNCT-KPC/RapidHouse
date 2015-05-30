Configuration for RapidHouse
============================
This section explains the configuration file for RapidHouse.

A format of the file is INI file format.
The file is parsed by Python ConfigParser module.


------
Notice
------

  - A base of a PATH is a PATH of the file when you set a relative PATH.
  - A command is run via Shell.
  - When you comment out a setting item, the value of the item will be *None*.


-------------
Setting items
-------------
This section explains setting items of the file.

[config] section
----------------
A settings for a configuration file for a server application.

input
	A PATH of a template of the configuration file for the server application.
output
	A outputted PATH of the configuration file for the server application.
backup
	A PATH for a backup.
	RapidHouse executes a command of *$ cp output backup*.


[eval] section
--------------
Settings for evaluating a server application.

apply
	A command for that applies the configuration for the server application.
wait
	A number of seconds for an interval of both applying and the evaluation.
bench
	A command for the evaluation.
remote
	the item for setting of that which run the *bench* on the local or the remote.
score
	A regular expression for extracting a evaluated result by the *bench*.
	RapidHouse use *$1* of a matched result.
soft_name
	A name of the server application.
	A default value of the *soft_name* is become a extracted string from the *apply*.


[ssh] section
-------------
A settings for an SSH connection with a server of tuning target.

server
	A string such as the URI scheme that indicate the server.
	If the *server* is the *None*, then RapidHouse will run the tuning on the local.
	The format of the *server* is as follows: <user>@<host>[:<port>].
pkey
	An RSA public key for the server.
	If the *pkey* is the *None*, then RapidHouse will use a password to authenticate.


[algorithm] section
-------------------
A settings for an algorithm for tuning.

type
	A name of the algorithm.
	The only selectable name is "GA" at the moment.
	N o d a - c h a n   c a b i n e t .


[log] section
-------------
A settings for logging of tuning.

level
	A level of the log.
	You should set either "info" or "debug".
file
	A PATH of the log file of RapidHouse.

-------
Example
-------
The file example as follows:

.. literalinclude:: ../../rapidhouse/rapid_house.ini

