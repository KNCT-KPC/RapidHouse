# -*- coding: utf-8 -*-
import order
import re


class ParseConfig(object):
	"""
	This class parse a template file of a configuration file for a server application.

	the `self.input` of the instance variable is the template file for the server application.
	the `self.abstract` of the instance variable is a intermediate representation for the tuning.
	the `self.kvv` of the instance variable is a information of a parameters.
	the `self.kvp` of the instance variable is a information of the parameters for the Information-DB.

	:param input: the template file for the server application.
	"""

	def __init__(self, input):
		self.input = input + "\n"
		self.abstract = None
		self.kvv = None
		self.kvp = None

	def parse(self):
		"""
		Parse the configuration file.
		"""
		self.abstract = self.input
		self.kvv = {}	# Key! Value! Variable!	{"hoge": [Value, Range, Visitor]}
		self.kvp = {}	# Key! Value! Paramater!

		# Escape
		self.abstract = self.abstract.replace('%', '%%')

		# Create KVV
		# Find `#{ hoge[min,max] }`
		for match in re.finditer(r'#{\s*(.+?)\s*(?:\[\s*([+-]?(?:inf|\d+))?\s*[:,]\s*([+-]?(?:inf|\d+))?\s*\])?\s*}', self.abstract):
			key = match.group(1)
			value = None
			visit = 1

			mini = maxi = None
			if match.group(2) is not None and 'inf' not in match.group(2):
				mini = int(match.group(2))
			if match.group(3) is not None and 'inf' not in match.group(3):
				maxi = int(match.group(3))

			if key in self.kvv:
				old = self.kvv[key][1]	# range
				if mini is None and old['min'] is not None:
					mini = old['min']
				if mini is not None and old['min'] is not None and old['min'] > mini:
					mini = old['min']
				if maxi is None and old['max'] is not None:
					maxi = old['max']
				if maxi is not None and old['max'] is not None and old['max'] < maxi:
					maxi = old['max']

				visit += self.kvv[key][2]	# visitor

			range = order.renge(mini, maxi)
			self.kvv[key] = [value, range, visit]
			self.abstract = self.abstract.replace(match.group(0), "%%(%s)s" % key)

		# Create KVP
		# Find `Paramater = Value`
		NEWLINE = ["\r\n", "\n", ";"]
		SEPARATOR = ["\t", " ", ":", "=", "=>"]
		ns = NEWLINE + SEPARATOR
		item_reg = re.compile(r'[\s]*(.+?)\s*(?::|=>|=| |\t)\s*(.+?)(?:\r\n|\n|;)+')
		var_reg = re.compile(r'%\((.+?)\)s')

		for match in var_reg.finditer(self.abstract):
			match_start = match.start()
			idx = -1
			while (True):
				break_flg = True
				for s in NEWLINE:
					idx = self.abstract.rfind(s, 0, match_start)
					if idx == -1:
						continue
					if s != ";":
						break
					idx -= 1
					if idx == -1:
						continue
					if self.abstract[idx] in ns:
						match_start = idx
						break_flg = False
					idx += 2
				if break_flg:
					break

			if idx == -1:
				idx = 0
			m = item_reg.search(self.abstract, idx)

			key = m.group(1)
			value = m.group(2).strip()
			if key.startswith(";") or key.startswith("#") or key.startswith("//"):
				self.kvv[match.group(1)][2] -= 1
				continue
			self.kvp[key] = value

		# Modify KVP
		# for `Timeout 10	# #{old}`
		comm_reg = re.compile(r'\s+(?:#|;|//).*$')
		for k, v in self.kvp.items():
			comment = comm_reg.search(v)
			if comment is None:
				continue
			self.kvp[k] = v.replace(comment.group(0), "").strip()
			if len(self.kvp[k]) == 0 or var_reg.search(self.kvp[k]) is None:
				del self.kvp[k]
			for match in var_reg.finditer(v):
				self.kvv[match.group(1)][2] -= 1

		# Modify KVV
		# Bocchi is dead.
		for k, v in self.kvv.items():
			if v[2] > 0:
				continue
			del self.kvv[k]
