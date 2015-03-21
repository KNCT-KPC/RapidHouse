# -*- coding: utf-8 -*-
"""
Utility command
"""
import subprocess
import math
import random


def run(cmd, conn=None):
	"""
	Execute the external command via the shell.

	:param str cmd: the external command with argument.
	:param conn: the SSH connection. If it is `None`, then will execute on the local.

	:rtype: dictionary
	:return: {'code': RETURN_CODE, 'stdout': str or None, 'stderr': str or None}
	"""
	if conn is None:
		# Local
		p = subprocess.Popen(
			cmd,
			stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
			shell=True
		)

		code = p.wait()
		stdout, stderr = p.communicate()
	else:
		# SSH
		stdin, stdout, stderr = conn.exec_command(cmd)
		code = stdout.channel.recv_exit_status()

		if stdout is not None:
			stdout = stdout.read()
		if stderr is not None:
			stderr = stderr.read()

	if not stdout:
		stdout = None
	if not stderr:
		stderr = None
	return {'code': code, 'stdout': stdout, 'stderr': stderr}


def renge(mini=None, maxi=None):
	"""
	Nyanpass~.
	This `renge` is more useful than the `range`.

	:param mini: the lower limit.
	:param maxi: the upper limit.

	:rtype: dictionary
	:return: {'min': mini, 'max': maxi}

	:raises ValueError: when `mini > max`.
	"""

	if (mini is not None and maxi is not None) and mini > maxi:
		raise ValueError("Relationship between `mini` and `maxi` is reversed.")

	return {'min': mini, 'max': maxi}


def round_range(num, ren):
	"""
	Round the number by the `renge`.
	If you define the `renge`, then the return-value will be periodic.
	If you define only one of either min or max, then the return-value will be symmetric.
	If you don't define the `renge`, then the return-value is always the input-value.

	:param num: a number.
	:param ren: the return-value of the `renge`.

	:return: the rounded number.
	"""
	mini = ren['min']
	maxi = ren['max']

	# 両方未定義
	if (mini is None) and (maxi is None):
		return num

	# どっちか未定義
	# mini や maxi の軸で折り返す
	if (mini is None) and (maxi is not None):
		return (-num + 2 * maxi) if num > maxi else num
	if (mini is not None) and (maxi is None):
		return (-num + 2 * mini) if num < mini else num

	# 定義済み
	# (num * n) % maxi == mini となってしまうので、maxi と完全一致だけは通してやろう
	# 以降は、mini を優先
	if maxi == num:
		return num

	# Pythonの剰余は「最小非負剰余」。いいね?
	return ((num - mini) % (maxi - mini)) + mini


def randint_range(ren, mini=0, maxi=65535):
	"""
	It is the `random.randint` that use `round_range`.

	:param ren: the `renge`.
	:param int mini: the lower limit for the `random.rantint`.
	:param int maxi: the upper limit for the `random.rantint`.

	:rtype: int
	:return: the random number.
	"""
	return round_range(random.randint(mini, maxi), ren)


def norm(vec1, vec2):
	"""
	Calculate the norm between lists.

	:param list vec1: a list.
	:param list vec2: a list.

	:rtype: float
	:return: the norm.
	"""
	return math.sqrt(sum([(v1 - v2) ** 2 for (v1, v2) in zip(vec1, vec2)]))
