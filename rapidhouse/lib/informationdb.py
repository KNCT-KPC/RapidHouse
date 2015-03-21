# -*- coding: utf-8 -*-
import order
import requests
import json
import shlex
import re


class InformationDb(object):
	"""
	It is class that to use the Information-DB for RapidHouse.

	:param ssh_conn: the SSH connection with the server of tuning target.
	:param soft_name: the name of server application.
	:param bench_cmd: the command of to evaluation of that the server of tuning target.
	:param config: Instance of `parameter.Parameter`.
	:param host: the hostname of the Information-DB.
	:param port: the HTTP port number of the Information-DB.
	"""

	def __init__(self, ssh_conn, soft_name, bench_cmd, config, host="rapidhouse-db.nitkc.org", port=80):
		self.config = config
		self.conn_error = False

		# パラメータの取得
		param = {}
		param["soft_name"] = soft_name
		param["bench_cmd"] = json.dumps(self.__cmd_parse(bench_cmd))
		param["proper_param_name"] = json.dumps([config.get_param_name(n) for n in config.get_param_list()])

		# CPU
		j = 0
		for line in order.run("lscpu", ssh_conn)["stdout"].splitlines():
			j += 1

			if j == 1:
				key = "cpu_arch"
			elif j == 4:
				key = "cpu_cores"
			elif j == 10:
				key = "cpu_vendor"
			elif j == 11:
				key = "cpu_product"	# family
			elif j == 12:
				key = "cpu_product"	# model
			elif j == 14:
				key = "cpu_freq"
			else:
				continue

			value = line.split(":")[1].strip()
			if j == 4:
				value = int(value)
			if j == 14:
				value = float(value)

			if key in param:
				param[key] += value
			else:
				param[key] = value

		# Memory
		j = 0
		param["mem_size"] = 0
		for line in order.run("free -m", ssh_conn)["stdout"].splitlines():
			j += 1
			if not (j == 2 or j == 4):
				continue

			value = float(line.split(":")[1].strip().split(" ")[0].strip())
			if j == 4:
				value *= 0.1
			param["mem_size"] += value


		# リクエスト投げる
		self.host = host
		self.port = port
		self.session = requests.session()

		try:
			r = self.session.post(self.__uri('systems'), params=param, headers={'X-EVIL': '0'})
			if r.status_code != 200:
				raise ValueError('Invalid param.')
		except:
			self.conn_error = True


	def get_param(self, count=None):
		"""
		Get the proper parameters.

		:param int count: the length of the parameters that you want to get. `None` is infinite.

		:return: the proper parameters.
		"""
		if self.conn_error:
			return []

		uri = self.__uri('params')
		if count is not None:
			r = self.session.get(uri, params={'count': count}, headers={'X-EVIL': '0'})
		else:
			r = self.session.get(uri)
		if r.status_code != 200:
			raise ValueError('Invalid.')
		return json.loads(r.text)


	def post_param(self, param):
		"""
		Post the proper parameter.

		:param dictionary param: the proper param.
		"""
		if self.conn_error:
			return

		if param['score'] in [-1, '-1']:
			return

		r = self.session.post(self.__uri('params'), params=param, headers={'X-EVIL': '0'})
		if r.status_code >= 400:
			raise ValueError('Invalid.')


	def __uri(self, path):
		"""
		Generate the URI for a request.

		:param str path: for example, `systems`, `params` and ..., etc.
		"""
		return "http://%s:%d/%s" % (self.host, self.port, path)


	def __cmd_parse(self, line):
		"""
		Parse the command-line.

		:param str line: the command-line.

		:rtype: dictionary
		:return: set of the command name and the argument.
		"""
		lst = shlex.split(line)

		cmd = lst[0]

		pre_arg = []
		for l in lst[1:]:
			if not l.startswith("-"):
				pre_arg.append(l)
				continue

			r = re.compile("\d")
			m = r.search(l)
			if m is None:
				pre_arg.append(l)
				continue

			pre_arg.append(l[0:m.start()])
			pre_arg.append(l[m.start():])

		arg = {}
		name = None
		next_is_name = True
		for a in pre_arg:
			if next_is_name:
				if not a.startswith("-"):
					continue
				arg[a] = ""
				name = a
			else:
				arg[name] += a
			next_is_name = not next_is_name

		return {'cmd': cmd, 'arg': arg}
