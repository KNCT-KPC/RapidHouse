# -*- coding: utf-8 -*-
import order
import parseconfig
import copy


class Parameter(object):
	"""
	This class edit the configuration file for the server application.

	:param str in_file: the local PATH of the template file.
	:param str out_file: It is the configuration file PATH for the server application which the PATH is either the remote PATH or the local PATH.
	"""

	def __init__(self, in_file, out_file):
		self.input = in_file
		self.output = out_file

		f = open(self.input, "r")
		contents = f.read()
		f.close()
		self.config = parseconfig.ParseConfig(contents)
		self.config.parse()

		self.reset()


	def reset(self):
		"""
		Reset the parameters.
		"""
		self.para = copy.deepcopy(self.config.kvv)


	def set(self, name, value):
		"""
		Set the parameter.

		:param name: the key.
		:param value: the value.
		"""
		self.para[name][0] = order.round_range(value, self.para[name][1])


	def write(self):
		"""
		Generate string for writing.

		:rtype: str
		:return: the string that the parameter is embedded.
		"""
		tmp = dict([(k, v[0]) for k, v in self.para.items()])
		return self.config.abstract % tmp


	def get_outfile_path(self):
		"""
		Getter for the PATH for outputting of file.

		:rtype: str
		:return: the PATH for outputting of file.
		"""
		return self.output


	def get_param_list(self):
		"""
		Return the list of the parameters name.

		:rtype: list
		:return: the list of the parameters name.
		"""
		return [k for k, v in self.para.items()]


	def get_param_range(self, name):
		"""
		Return the range of the parameter.

		:param name: the key.

		:return: the range of the parameter.
		"""
		return self.para[name][1]


	def get_param_name(self, name):
		"""
		Return the proper parameter name.

		:param name: the parameter name that is set by the user.

		:return: the proper parameter name.
		"""
		search = "%%(%s)" % name

		for k, v in self.config.kvp.items():
			if search not in v:
				continue
			return k

		return None
