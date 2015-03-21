# -*- coding: utf-8 -*-
import order
import informationdb
import os
import time
import paramiko
import re
import getpass
import tempfile
import scp
import json
import shutil
import math


class Tune():
	"""
	This class handle a tuning.

	:param interface: a instance of the `ui.Ui`.
	:param algo: a reified instance of the `alg.Algorithm`.
	:param config: a instance of the `parameter.Parameter`.
	:param rc: a instance of the `rapidconfig.RapidConfig`.
	:param tuple group: a group of a initial solutions.
	"""

	def __init__(self, interface, algo, config, rc, group):
		self.interface = interface
		self.algorithm = algo
		self.config = config
		self.rc = rc
		self.seq = config.get_param_list()
		self.idb = None
		self.base_group = group
		self.bests = []


	def cost(self, pop):
		"""
		Evaluate of a solution.

		:param list pop: the solution.

		:return: either `-1` or a cost of the solution.
		"""
		# 反映
		self.write(pop)
		r = order.run(self.rc.apply_cmd, self.ssh_conn)
		self.interface.notice_debug('apply', r)
		if r['code'] != 0:
			return self.interface.notice_score(-1, pop)
		time.sleep(self.rc.wait_time)

		# 計測
		if self.rc.bench_remote:
			result = order.run(self.rc.bench_cmd, self.ssh_conn)
		else:
			result = order.run(self.rc.bench_cmd)
		self.interface.notice_debug('bench', result)
		if result["code"] != 0 or result["stdout"] is None:
			return self.interface.notice_score(-1, pop)

		# 抽出
		r = re.compile(self.rc.score_reg)
		match = r.search(result["stdout"])
		if match is None:
			return self.interface.notice_score(-1, pop)

		# 終わり
		try:
			return self.interface.notice_score(float(match.group(1)), pop)
		except:
			return self.interface.notice_score(-1, pop)


	def run(self):
		"""
		A thread of the tuning.
		"""
		if self.rc.server['host'] is None:
			# Local
			self.ssh_conn = None
		else:
			# Remote
			conn = paramiko.SSHClient()
			conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

			passwd = ''
			if self.rc.server['pkey'] is None:
				passwd = getpass.getpass('SSH Password: ')
				conn.connect(username=self.rc.server['user'], password=passwd, hostname=self.rc.server['host'], port=self.rc.server['port'])
			else:
				try:
					conn.connect(username=self.rc.server['user'], hostname=self.rc.server['host'], port=self.rc.server['port'], key_filename=self.rc.server['pkey'])
				except (paramiko.PasswordRequiredException, paramiko.ssh_exception.SSHException):
					passwd = getpass.getpass('SSH Private Key Passphrase: ')
					conn.connect(username=self.rc.server['user'], hostname=self.rc.server['host'], port=self.rc.server['port'], password=passwd, key_filename=self.rc.server['pkey'])
			del passwd
			l4 = conn.get_transport()
			l4.set_keepalive(30)
			self.ssh_conn = conn

		# バックアップ
		if self.rc.backup is not None:
			if self.ssh_conn is None:
				f = shutil.copyfile
			else:
				scp_conn = scp.SCPClient(self.ssh_conn.get_transport())
				f = scp_conn.get
			f(self.config.get_outfile_path(), self.rc.backup)

		# 情報データベース
		if self.idb is None:
			self.idb = informationdb.InformationDb(self.ssh_conn, self.rc.soft_name, self.rc.bench_cmd, self.config)
			self.algorithm.init_group(self.idb, self.base_group)

		# 開始
		while True:
			group = self.algorithm.get_group()
			scores = sorted([(self.cost(p), p) for p in group], reverse=True)

			# 送信
			best = sorted(scores, reverse=True)[0]
			param = {}
			for (n, p) in zip(self.seq, best[1]):
				param[self.idb.config.get_param_name(n)] = p

			self.idb.post_param({"score": best[0], "propar_param": json.dumps(param)})
			self.interface.notice_best(best[0], best[1])

			# エラー判定
			if best[0] in [-1, '-1']:
				raise StandardError('Check both your server and a command on a configuration file for RapidHouse.')

			# 収束判定
			MAXSIZE = 10
			if len(self.bests) >= MAXSIZE:
				self.bests.pop(0)
			self.bests.append(best[1])
			if len(self.bests) == MAXSIZE:
				d = 0.0
				for i in range(MAXSIZE - 1):
					tmp = 0.0
					for p1, p2 in zip(self.bests[i], self.bests[i + 1]):
						tmp += (p2 - p1) ** 2
					d += math.sqrt(tmp)
				self.interface.debug_print('>[score:d]> Distance: %s%s' % (d, os.linesep))
				if d < 1:
					self.interface.stop()

			self.algorithm.next(scores)
		if self.ssh_conn is not None:
			self.ssh_conn.close()


	def write(self, pop=None):
		"""
		Write out a configuration file for a server application.

		:param pop: a population.
		"""
		if pop is None and len(self.bests) == 0:
			return
		if pop is None:
			pop = self.bests[-1]

		self.config.reset()
		for (n, p) in zip(self.seq, pop):
			self.config.set(n, p)

		tmp = tempfile.mkstemp()
		fp = os.fdopen(tmp[0], "w")
		fp.write(self.config.write())
		fp.close()

		if self.ssh_conn is None:
			f = shutil.copyfile
		else:
			scp_conn = scp.SCPClient(self.ssh_conn.get_transport())
			f = scp_conn.put
		f(tmp[1], self.config.get_outfile_path())
		os.remove(tmp[1])
