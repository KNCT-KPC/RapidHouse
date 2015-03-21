# -*- coding: utf-8 -*-
from ..lib import order


def test_round_range():
	assert 0 == order.round_range(0, {'min': None, 'max': None})
	assert 114514 == order.round_range(114514, {'min': None, 'max': None})
	assert 114514 == order.round_range(-114514, {'min': 0, 'max': None})
	assert -114514 == order.round_range(114514, {'min': None, 'max': 0})
	assert 58 == order.round_range(114514, {'min': 0, 'max': 114})
