Tutorial
========
This section is a tutorial for RapidHouse.

------------
Installation
------------
This section explains how to install RapidHouse via GitHub.

.. code-block:: bash

   $ pip install git+https://github.com/KNCT-KPC/RapidHouse


It's so easy.


-----
Usage
-----
This section explains how to tune Apache HTTP Server.


Prepare a configuration file for the server application.
--------------------------------------------------------
You must prepare the configuration file for the server application.

.. code-block:: bash

   $ scp user@server:/etc/httpd/conf/httpd.conf test/httpd.conf
   $ vim test/httpd.conf

Then, you change some parameter value as follows:

.. literalinclude:: httpd.diff


Prepare a configuration file for RapidHouse.
---------------------------------------------
You must prepare the configuration file for RapidHouse as follows:

.. literalinclude:: ../../rapidhouse/rapid_house.ini

Then, save the file as "rapid_house.ini".
See also :doc:`rapidconfig` .


Run
---
Be caught up in the darkness!

.. code-block:: bash
   
   $ rapidhouse rapid_house.ini
   $ vim test/httpd.conf


When you satisfied with a result of tuning, you should stop RapidHouse.
In Addition, RapidHouse stops when the approximate solution is unchanged.

