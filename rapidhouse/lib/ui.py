# -*- coding: utf-8 -*-
from ..algorithm import ga
import parameter
import tune
import sys
import os
import signal
import time


class Ui(object):
	"""
	This class handle both the CUI and the GUI.

	:param rc: a instance of the `rapidconfig.RapidConfig`.
	"""

	def __init__(self, rc):
		self.tuner = None
		self.seq = None
		self.config = None

		self.rc = rc
		self.fp = None if rc.log_file is None else open(rc.log_file, "a")


	def get_input(self, msg, test=None):
		"""
		Get a input from a user.

		:param str msg: a outputted message on the console.
		:param test: for a unit-test. Unless the `test` is the `None`, then the return-value is the `test`.

		:return: the input-value from the user.
		"""
		return test if test is not None else raw_input("%s: " % msg)


	def get_boolean(self, msg, test=None):
		"""
		Get a boolean input from a user.

		:param str msg: a outputted message on the console.
		:param test: for a unit-test. Unless the `test` is the `None`, then the return-value is the `test`.

		:return: the boolean input-value from the user.
		"""
		if test is not None:
			return test

		tmp = self.get_input(msg + "[y/N]")
		return tmp in ["y", "yes"]


	def notice_score(self, score, pop):
		"""
		Call self.__notice(), and return a score.

		:param score: the score.
		:param pop: a population that having the score.

		:return: the score.
		"""
		self.__notice("Score", score, pop)
		return score


	def notice_best(self, best_score, pop):
		"""
		Call self.__notice(), and return a best score.

		:param best_score: the best score.
		:param pop: a population that having the best score.

		:return: the best score.
		"""
		self.__notice("Best", best_score, pop)
		return best_score


	def notice_debug(self, type, contents):
		"""
		Give notice for debugging.

		:param str type: a identifier.
		:param dictionary contents: a result of a executed command.
		"""
		if self.rc.log_level != "debug":
			return
		for s in ['stdout', 'stderr']:
			if contents[s] is None:
				continue
			for l in contents[s].splitlines():
				self.__print(">[%s:%s]> %s%s" % (type, s, l, os.linesep))


	def debug_print(self, string):
		"""
		Call self.__print() for debugging.

		:param str string: the string.
		"""
		if self.rc.log_level != "debug":
			return
		self.__print(string)


	def __notice(self, type, score, pop):
		"""
		Give notice of both a score and a population.

		:param str type: a identifier.
		:param score: the score.
		:param pop: a population that having the best score.
		"""
		tmp = ''
		for (n, p) in zip(self.seq, pop):
			tmp += "%s=%s," % (self.config.get_param_name(n), p)
		tmp = tmp[0:-1]
		self.__print(">[%s:%s]> %s %s%s" % ('score', 'normal' if type == 'Score' else 'best', score, tmp, os.linesep))
		if self.fp is None:
			return

		if type == 'Best':
			print '---'
		print '%s %s %s' % (type, score, tmp)
		if type == 'Best':
			print '---'


	def __print(self, string):
		"""
		Print a string to either the `STDOUT` or a log-file.

		:param str string: the string.
		"""
		t = time.strftime('%Y/%m/%d %H:%M:%S')

		f = sys.stdout if self.fp is None else self.fp
		f.write("<%s%s" % (t, string))
		f.flush()


	def manager(self):
		"""
		Manage a tuning.
		"""
		self.config = parameter.Parameter(self.rc.input, self.rc.output)
		self.seq = self.config.get_param_list()

		# 範囲
		ranges = [self.config.get_param_range(n) for n in self.seq]

		# アルゴリズムの準備
		group = ([], 10)

		if self.rc.alg_type == "GA":
			algorithm = ga.GaSuneko(ranges)
		else:
			raise ValueError("Invalid Algorithm type: %s" % self.rc.alg_type)

		# 開始していく
		signal.signal(signal.SIGINT, self.stop)
		self.tuner = tune.Tune(self, algorithm, self.config, self.rc, group)
		self.tuner.run()


	def stop(self, *args):
		"""
		Stop a tuning.
		"""
		sys.stderr.write('SIGINT%s' % os.linesep)
		self.tuner.write()
		if self.fp is not None:
			self.fp.close()
		exit()
