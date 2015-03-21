# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
	name = 'rapidhouse',
	version = '0.0.1',
	description = 'Automated tuning-tool for a server application.',
	license = 'MIT License',
	author = 'KPC',
	author_email = 'yuke1222@gmail.com',
	url = 'http://rapidhouse.nitkc.org/',
	keywords = 'ga tune server automation',
	packages = find_packages(),
	install_requires = ['paramiko', 'scp', 'requests'],
	entry_points = {
		'console_scripts': [
			'rapidhouse = rapidhouse.rapid_house:main'
		],
	},
)
