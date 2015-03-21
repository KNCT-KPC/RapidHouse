# -*- coding: utf-8 -*-
import os
import sys
import re
import ConfigParser
import shlex


class RapidConfig(object):
	"""
	This class parse a configuration file for RapidHouse.

	:param config_path: a PATH of the configuration file.
	"""

	def __init__(self, config_path):
		self.config_path = None if config_path == '-' else self.__nyanpath(config_path, os.getcwd())


	def parse(self):
		"""
		Parse the configuration file.
		"""
		self.config = ConfigParser.SafeConfigParser()
		if self.config_path is None:
			self.config.readfp(sys.stdin)
		else:
			self.config.read(self.config_path)

		prefix = os.getcwd() if self.config_path is None else os.path.dirname(self.config_path)
		self.input = self.__nyanpath(self.__get('config', 'input'), prefix)
		self.output = self.__get('config', 'output')
		backup = self.__get('config', 'backup', 'None')
		self.backup = None if backup == 'None' else self.__nyanpath(backup, prefix)

		self.apply_cmd = self.__get('eval', 'apply')
		self.wait_time = self.__get('eval', 'wait', 5, f=self.config.getfloat)
		self.bench_cmd = self.__get('eval', 'bench')
		self.score_reg = self.__get('eval', 'score')
		self.bench_remote = self.__get('eval', 'remote', default=True, f=self.config.getboolean)

		# SoftWare名
		tmp = shlex.split(self.apply_cmd)
		self.soft_name = self.__get('eval', 'soft_name', tmp[1] if tmp[0] == "service" else os.path.basename(tmp[0]))

		# SSH系
		server = self.__get('ssh', 'server', 'None')
		if server == 'None':
			server = None
		pkey = self.__get('ssh', 'pkey', 'None')
		if pkey == 'None':
			pkey = None

		self.server = {}
		if server is None:
			self.server['host'] = None
		else:
			m = re.match("^(.*?)@(.*?)(?:\:(\d+?))?$", server)
			if m is None:
				raise ValueError('Invalid. server = %s' % server)
			self.server['user'] = m.group(1)
			self.server['host'] = m.group(2)
			port = m.group(3)
			if port is None:
				port = 22
			self.server['port'] = int(port)
			self.server['pkey'] = None if pkey is None else self.__nyanpath(pkey, prefix)
			self.server['passwd'] = None

		self.alg_type = self.__get('algorithm', 'type', 'GA').upper()

		self.log_level = self.__get('log', 'level', 'info').lower()
		file = self.__get('log', 'file', 'None')
		if file == 'None':
			file = None
		self.log_file = None if file is None else self.__nyanpath(file, prefix)


	def __get(self, section, option, default=None, f=None):
		"""
		Get a value of the configuration file.

		:param section: a key.
		:param option: a key.
		:param default: a default value of the value.
		:param f: a function that get the value.

		:return: the got value.
		"""
		if f is None:
			f = self.config.get

		if default is None:
			val = f(section, option)
		try:
			val = f(section, option)
		except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
			val = default

		if val == 'None':
			val = default

		if not isinstance(val, str):
			return val
		tmp = shlex.split(val)
		return tmp[0] if len(tmp) == 1 else val


	def __nyanpath(self, path, prefix):
		"""
		Get the absolute PATH.

		:param path: either the relative PATH or the absolute PATH.
		:param prefix: the current directory.

		:return: the absolute PATH.
		"""
		for f in [os.path.expanduser, lambda p: os.path.abspath(prefix + '/' + p)]:
			if path.startswith('/'):
				break
			path = f(path)
		return path
