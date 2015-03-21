# -*- coding: utf-8 -*-
import os
from ..lib import parseconfig


def test_lib_class_parseconfig():
	base = os.path.abspath(os.path.dirname(__file__)) + '/'

	kvv = {'keep_de_deeen': [None, {'max': 50, 'min': 0}, 1], 'sv_lmt': [None, {'max': 512, 'min': 0}, 1], 'max_cli': [None, {'max': 512, 'min': 0}, 1], 'min_spare_sv': [None, {'max': 10, 'min': 0}, 1], 's_servers': [None, {'max': 50, 'min': 0}, 1], 'de_deeeen': [None, {'max': 1200, 'min': 0}, 1], 'max_sp_sv': [None, {'max': 15, 'min': 0}, 1], 'uhehe': [None, {'max': 10000, 'min': 0}, 1], 'keep_a_live': [None, {'max': 1000, 'min': 0}, 1]}
	kvp = {'MaxSpareServers': '%(max_sp_sv)s', 'MinSpareServers': '%(min_spare_sv)s', 'ServerLimit': '%(sv_lmt)s', 'StartServers': '%(s_servers)s', 'MaxClients': '%(max_cli)s', 'Timeout': '%(de_deeeen)s', 'KeepAliveTimeout': '%(keep_de_deeen)s', 'MaxKeepAliveRequests': '%(keep_a_live)s', 'MaxRequestsPerChild': '%(uhehe)s'}

	for f in ['httpd.conf', 'apache2.conf']:
		tmp = __sub(base + 'httpd.conf')
		assert tmp.kvv == kvv
		assert tmp.kvp == kvp


def __sub(input):
	f = open(input, "r")
	contents = f.read()
	f.close()

	tmp = parseconfig.ParseConfig(contents)
	tmp.parse()

	return tmp
