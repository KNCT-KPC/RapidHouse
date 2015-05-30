RapidHouse
==========
An automated tuning tool for a server application by GA(Genetic Algorithm).
RapidHouse was published in [Programming Contest](http://www.procon.gr.jp/).

An innovative feature of RapidHouse is to use an own database by communicating with the internet.
The database has information that an approximate solution for the server application.
You quickly get the solution by the database.


## Quick Try

We prepared a base image for Vagrant that RapidHouse and WordPress are installed.
This image is based on [2creatives/vagrant-centos CentOS 6.5 x86_64 Minimal](https://github.com/2creatives/vagrant-centos/releases/tag/v6.5.3).
You use this image as follows:

    $ wget http://rapidhouse.nitkc.org/vagrant/v0.0.1/Vagrantfile
    $ vagrant up
    $ vagrant ssh
    [vagrant@vagrant-centos65 ~]$ cd rapidhouse
    [vagrant@vagrant-centos65 ~]$ sudo rapidhouse rapid_house.ini
    Score 9.88 KeepAliveTimeout=13....
    Score 10.1 KeepAliveTimeout=4.....
	 :
    ^C
    SIGINT
   
I wish you the best.
But the best solution might have already derived by the database.


## How to use

    $ sudo pip install git+https://github.com/KNCT-KPC/RapidHouse
    $ rapidhouse rapidhouse_config_file.ini

## See also

  * [RapidHouse’s documentation](http://rapidhouse.nitkc.org/)

## Error handling

    $ sudo apt-get python-dev python-setuptools # or `yum install python-devel python-setuptools`
    $ sudo easy_install --upgrade pip
    $ sudo pip install --upgrade setuptools
    $ sudo pip install --upgrade setuptools distribute

## Contact us

In Japanese or very easy English, please.

### Academic contact

  * National Institute of Technology, Kushiro College / 釧路工業高等専門学校
  * Advanced Course / 専攻科
  * Yuusuke Morikoshi / 森越友祐
  * mailto: base64\_decode("czE0MDcxM0BjYy5rdXNoaXJvLWN0LmFjLmpw")

### Other contact

  * `whois nitkc.org`
  * `whois -h whois.charlestonroadregistry.com xn--vckq4ald8kl4jk9f.xn--q9jyb4c`

