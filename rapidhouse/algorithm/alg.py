# -*- coding: utf-8 -*-
from ..lib import order
import copy
import random


class Algorithm(object):
	"""
	This class is abstracting that algorithm for searching the solution of a combination.
	"""

	def __init__(self, ranges):
		"""
		:param list ranges: list of `order.renge`.
		"""
		self.ranges = ranges


	def init_group(self, idb, basic):
		"""
		Initialize a group of solution.

		:param idb: Instance of `informationdb.InformationDb`.
		:param tuple basic: the basic[0] is list of the basic groups. the basic[1] is the group length.
		"""
		self.group = copy.deepcopy(basic[0])
		size = basic[1] - len(self.group) # 残サイズ
		i_size = int(0.5 * size)	# 情報データベースで取ってくる数

		# 情報データベースへ取りに行く
		if (i_size) > 0:
			for g in idb.get_param(i_size):
				self.group.append([order.round_range(g["param"][idb.config.get_param_name(p)], r) for p, r in zip(idb.config.get_param_list(), self.ranges)])

		# 補完
		for i in range(basic[1] - len(self.group)):
			if random.random() < 0.5 and len(self.group) != 0:
				index = random.randint(0, len(self.group) - 1)
				self.group.append(self.mutate_gauss(self.group[index], sum(self.group[index]) / float(len(self.group[0]))))
			else:
				self.group.append([order.randint_range(r) for r in self.ranges])


	def get_group(self):
		"""
		Getter for the group of solution.

		:return: the group of solution.
		"""
		return self.group


	def mutate_gauss(self, lst, sigma):
		"""
		Mutate with a normal random number.

		:param list lst: a list.
		:param int sigma: Standard deviation.

		:rtype: list
		:return: the mutated list.
		"""
		return [order.round_range(int(random.gauss(v, sigma)), r) for (v, r) in zip(lst, self.ranges)]


	def random_indexes(self, lst):
		"""
		Return list of random indexes.

		:param list lst: a list.

		:rtype: list
		:return: list of random indexes.
		"""
		indexes = range(random.randint(1, len(lst)))
		random.shuffle(indexes)
		return indexes
