# -*- coding: utf-8 -*-
import alg
from ..lib import order
import random
import copy
import math


class GaSuneko(alg.Algorithm):
	"""
	This class is using GA as that algorithm for searching the solution of a combination.

	:param list ranges: Pass to the parent class.
	:param float mutprob: the mutation probability.
	:param float elite: the percentage of surviving a elite.
	:param float step: the amount of change for the mutation.
	"""

	# 初期化
	def __init__(self, ranges, mutprob=0.3, elite=0.2, ranran=0.3):
		alg.Algorithm.__init__(self, ranges)
		self.mutprob = mutprob
		self.elite = elite
		self.step = 1
		self.ranran = ranran


	# 次世代
	def next(self, scores):
		"""
		Generate the population of the next generation.

		:param tuple scores: set of the population and the cost of the population.
		"""
		ranked = [v for (s, v) in sorted(scores, reverse=True)]
		size = len(ranked)
		topelite = int(self.elite * size)

		# つくってあそぼ
		j = 0
		next_generation = copy.deepcopy(ranked[0:topelite])
		for i in range(int(self.ranran * size)):
			next_generation.append([order.randint_range(r) for r in self.ranges])
		while len(next_generation) < size:
			# 対象
			if random.random() < 0.75:
				target = ranked
			else:
				target = next_generation
			t_len = len(target)

			if random.random() < self.mutprob or t_len == 1:
				# 突然変異
				c = random.randint(0, t_len - 1)
				tmp = self.mutate(copy.deepcopy(target[c]))
			else:
				if random.random() < 0.5 and t_len >= 3:
					# UNDX
					try:
						p1, p2, p3 = random.sample(target, 3)
						tmp = self.undx(copy.deepcopy(p1), copy.deepcopy(p2), copy.deepcopy(p3))
					except:
						continue
				else:
					# 交叉
					p1, p2 = random.sample(target, 2)
					tmp = self.crossover(copy.deepcopy(p1), copy.deepcopy(p2))

			# 重複を避ける
			if (tmp not in next_generation) or j > 10:
				next_generation.append(tmp)
				j = 0
			else:
				j += 1

		self.group = next_generation


	# 突然変異
	def mutate(self, pop):
		"""
		Mutate the population.

		:param list pop: the population.
		:rtype: list
		:return: the mutated population.
		"""
		indexes = super(GaSuneko, self).random_indexes(pop)

		# ＿人人人人 人人人＿
		# ＞　突然の変異　 ＜
		# ￣Y^Y^Y^Y^Y^Y^Y^Y￣
		for index in indexes:
			step = int(pop[index] + 0.1 * (self.step if random.random() < 0.5 else -self.step))
			pop[index] = order.round_range(pop[index] + step, self.ranges[index])

		return pop


	# 交叉
	def crossover(self, pop1, pop2):
		"""
		Crossover the populations.

		:param list pop1: a population.
		:param list pop2: a population.
		:rtype: list
		:return: the crossedover population.
		"""
		if random.random() < 0.5:
			pop1, pop2 = pop2, pop1

		indexes = super(GaSuneko, self).random_indexes(pop1)
		for index in indexes:
			pop1[index] = pop2[index]

		return pop1


	# UNDXによる子の作成
	def undx(self, parent1, parent2, parent3):
		"""
		Reproduce with UNDX algorithm.
		http://mikilab.doshisha.ac.jp/dia/research/person/takapy/2001/semi/Weekly_Report/06_20010716/report/report.html

		:param list parent1: a population.
		:param list parent2: a population.
		:param list parent3: a population.
		:rtype: list
		:return: the reproduced population.
		"""
		length = len(parent1)
		alpha = 0.5 ** 2
		beta = (0.35 ** 2) / length

		p_v = [(p1 + p2) * 0.5 for (p1, p2) in zip(parent1, parent2)]
		d_v = [(p1 - p2) for (p1, p2) in zip(parent1, parent2)]

		p3_p1 = [(p3 - p1) for (p3, p1) in zip(parent3, parent1)]
		d_a = float(sum([x ** 2 for x in p3_p1]))
		d = [math.sqrt(d_a - (math.fabs(x) * d_a) / ((x + 0.001) ** 2)) for x in d_v]

		e_v = [x / (float(math.sqrt(sum([x ** 2 for x in d_v]))) + 0.001) for x in d_v]

		child = []
		for i in range(length):
			tmp = d[i] * float(sum([random.gauss(0, beta) * e for e in e_v]))
			child.append(order.round_range(int(p_v[i] + random.gauss(0, alpha) * d_v[i] + tmp), self.ranges[i]))
		return child
