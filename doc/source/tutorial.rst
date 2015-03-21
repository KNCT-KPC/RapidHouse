Tutorial
========
This section explain RapidHouse.

--------
Overview
--------
RapidHouse is a automated tuning-tool for a server application that use GA(Genetic Algorithm) as a algorithm for tuning.
If you use RapidHouse, then a performance of the server application might be the improvement.

A innovative feature of RapidHouse is to use a own database by communicating with Internet.
The database has information that a approximate solution for the server application.
You quickly get the solution by the database.

If you didn't edit a program of RapidHouse, RapidHouse will sent the database a information as follows:

  - about Hardware
     - CPU Vendor
     - CPU Product Name
     - CPU Arch
     - CPU Frequency
     - CPU Cores
     - Memory Size
  - about Software
     - Server Application Name
     - Benchmark Command(**Don't include a your password.**)
  - about Solution
     - Approximate Solution
     - Result of benchmark

You should cooperate to improve the database.

// RapidHouse was published in Programming Contest(http://www.procon.gr.jp/).


------------
Installation
------------
This section explain how to install RapidHouse via GitHub.

.. code-block:: none

   $ pip install git+https://github.com/KNCT-KPC/RapidHouse


It's so easy.


-----
Usage
-----
This section explain how to tune Apache HTTP Server.


Prepare a configulation file for the server application.
--------------------------------------------------------
You must prepare the configulation file for the server application.

.. code-block:: none

   $ scp user@server:/etc/httpd/conf/httpd.conf test/httpd.conf
   $ vim test/httpd.conf

Then, you change some parameter value as follows:

.. literalinclude:: httpd.diff


Prepare a configulation file for RapidHouse.
---------------------------------------------
You must prepare the configulation file for RapidHouse as follows:

.. literalinclude:: ../../rapidhouse/rapid_house.ini

Then, save the file as "rapid_house.ini".
See also :doc:`rapidconfig` .


Run
---
Be caught up in the darkness!

.. code-block:: none
   
   $ rapidhouse rapid_house.ini
   $ vim test/httpd.conf


When you satisfied with a result of tuning, you should stop RapidHouse.
In Addition, RapidHouse stop when the approximate solution is unchanged.

